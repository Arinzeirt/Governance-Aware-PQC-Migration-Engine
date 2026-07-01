import { AuthUser, Document, DocumentResult } from '@app/common';
import {
  buildFindManyQuery,
  FindManyWrapper,
  FindOneWrapper,
  getAggregateValue,
  sleep,
} from '@app/helpers';
import { MailService, PaymentService, template } from '@app/services';
import { User } from '@app/users/entity';
import {
  ForbiddenException,
  forwardRef,
  Inject,
  Injectable,
  NotFoundException,
} from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { In, Not, Repository } from 'typeorm';
import { FollowTraders } from '../entities';
import { Trades } from '../entities/trader.entity';
import * as type from '../input';
import { TradeDefineService } from './define.service';
import { TradeJobWorker } from './trade-schedule.service';
import { ActivityService } from './activities.service';
import { BybitService } from './bybit.service';
import Big from 'big.js';
import { category } from '@app/wallets/input';

@Injectable()
export class TradesService {
  constructor(
    @InjectRepository(Trades) private readonly tradeRepo: Repository<Trades>,
    @InjectRepository(User) private readonly userRepo: Repository<User>,
    @InjectRepository(FollowTraders)
    private readonly follower: Repository<FollowTraders>,
    @Inject(forwardRef(() => TradeJobWorker))
    private readonly tradeJW: TradeJobWorker,
    private readonly activityFeed: ActivityService,
    private readonly mailService: MailService,
    private readonly ds: TradeDefineService,
    private readonly bybitService: BybitService,
    private readonly paymentService: PaymentService,
  ) {}

  async cancelTrade(tradeId: string, user: AuthUser): Promise<type.ITrades> {
    const trade = await this.tradeRepo.findOne({
      where: { id: tradeId, userId: user.id, status: Not(type.status.close) },
    });
    if (!trade) {
      throw new ForbiddenException('Trade not exist or Trade already close');
    }

    const cancelOnBybit = await this.bybitService.cancelOrder({
      category: 'linear',
      symbol: trade.symbol,
      orderId: trade.orderId,
      orderLinkId: trade.orderLinkId,
    });

    console.log(cancelOnBybit);

    if (cancelOnBybit.retCode === 110001) {
      throw new ForbiddenException(cancelOnBybit.retMsg);
    } else if (cancelOnBybit.retCode !== 0) {
      throw new ForbiddenException('unable to cancel trade at the moment ');
    }

    const currentPrice = await this.bybitService.getCurrentPrice(
      trade.asset,
      'linear',
    );

    if (!currentPrice) {
      throw new ForbiddenException('unable to cancel trade at the moment');
    }

    let realizedPnL: number;
    // Calculate position quantity: margin × leverage / entryPrice
    const positionQuantity = Big(trade.margin)
      .times(trade.leverage)
      .div(trade.entryPrice);

    if (trade.action === 'Buy') {
      // For Buy: (currentPrice - entryPrice) × quantity
      realizedPnL = Big(currentPrice)
        .sub(Big(trade.entryPrice))
        .times(positionQuantity)
        .toNumber();
    } else {
      // For Sell: (entryPrice - currentPrice) × quantity
      realizedPnL = Big(trade.entryPrice)
        .sub(Big(currentPrice))
        .times(positionQuantity)
        .toNumber();
    }

    console.log({ realizedPnL });

    const { outcome, tradeRoi } = this.ds.calculateTradeResults(
      trade.margin,
      realizedPnL,
    );

    trade.status = type.status.cancel;
    trade.exitPrice = currentPrice || 0;
    trade.realizedPnl = realizedPnL;
    trade.outcome = outcome;
    trade.tradeRoi = tradeRoi;

    // TODO fund the user balance
    const totalCredit = Big(trade.margin).add(Big(realizedPnL)).toNumber();

    if (totalCredit > 0) {
      void this.paymentService.internalCreditUser({
        amount: totalCredit,
        category: category.trade,
        user: trade.user,
      });
    }

    void this.activityFeed.create({
      title: 'Trade Closed',
      message: `${trade.asset} trade closed at: ${trade.exitPrice.toLocaleString()} - ${trade.realizedPnl}% P&L`,
      userId: user.id,
    });
    return this.tradeRepo.save(trade);
  }

  async findAll(query: type.findManyTrade): Promise<DocumentResult<Trades>> {
    const qb = this.tradeRepo.createQueryBuilder('trade');
    buildFindManyQuery(
      qb,
      'trade',
      this.filter(query),
      query.search,
      ['asset', 'symbol'],
      query.include,
      query.sort,
    );

    if (query.copiers === type.copiers.least) {
      const minCopiers = await getAggregateValue(
        qb.connection,
        'trades',
        'noOfCopiers',
        'MIN',
      );
      qb.andWhere('trade."noOfCopiers" = :minCopiers', { minCopiers });
    }

    if (query.copiers === type.copiers.most) {
      const maxCopiers = await getAggregateValue(
        qb.connection,
        'trades',
        'noOfCopiers',
        'MAX',
      );
      qb.andWhere('trade."noOfCopiers" = :maxCopiers', { maxCopiers });
    }

    // if (query.tradingTrade) {
    //   qb.andWhere('trade.noOfCopiers > :copiersThreshold', {
    //     copiersThreshold: 10,
    //   });
    // }

    if (query.timeFrame === 'top7days') {
      qb.andWhere('trade.noOfCopiers > :copiersThreshold', {
        copiersThreshold: 10,
      })
        .andWhere('trade.tradeRoi > :roiThreshold', { roiThreshold: 20 })
        .andWhere('trade.createdAt >= :recentDate', {
          recentDate: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000),
        }); // Last 7 days
    }

    return FindManyWrapper(qb, query.page, query.limit).then((data) => {
      data.data = data.data.map((item) => ({
        ...item,
        copiersProfit: item.getTotalProfitForCopies(),
      })) as any[];
      return data;
    });
  }

  async findOne(query: type.findOneTrade): Promise<Document<Trades>> {
    const { include, sort, ...filters } = query;
    // TODO risk ratio/reward
    return FindOneWrapper<Trades>(this.tradeRepo, {
      include,
      sort,
      filters,
    }).then((data) => {
      if (data) {
        (data.data as any).copiesProfit = data.data?.getTotalProfitForCopies();
      }
      return data;
    });
  }

  async getTradingStats(userId: string): Promise<type.TradingStats> {
    const now = new Date();
    const ninetyDaysAgo = new Date(now.getTime() - 90 * 24 * 60 * 60 * 1000);
    const thirtyDaysAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
    const sixtyDaysAgo = new Date(now.getTime() - 60 * 24 * 60 * 60 * 1000);

    // Base query
    const baseQuery = this.tradeRepo
      .createQueryBuilder('trade')
      .where('trade.creatorId = :userId', { userId });

    // Get open trades count
    const openTrades = await baseQuery
      .clone()
      .andWhere('trade.status IN (:...openStatuses)', {
        openStatuses: [type.status.pending, type.status['open']],
      })
      .getCount();

    // Get closed trades count
    const closedTrades = await baseQuery
      .clone()
      .andWhere('trade.status = :closedStatus', {
        closedStatus: type.status['close'],
      })
      .andWhere('trade.createdAt >= :ninetyDaysAgo', { ninetyDaysAgo })
      .getCount();

    // Get all trades for calculations
    const allTrades = await baseQuery.clone().getMany();

    // Calculate total PnL
    const totalPnL = allTrades.reduce((sum, trade) => {
      return sum + parseFloat(trade.realizedPnl.toString());
    }, 0);

    // Calculate win rate
    const completedTrades = allTrades.filter(
      (trade) => trade.outcome && trade.status === type.status['close'],
    );
    const winningTrades = completedTrades.filter(
      (trade) => trade.outcome === type.outcome['win'],
    );
    const winRate =
      completedTrades.length > 0
        ? (winningTrades.length / completedTrades.length) * 100
        : 0;

    // Calculate average ROI
    const averageROI =
      allTrades.length > 0
        ? allTrades.reduce((sum, trade) => sum + trade.tradeRoi, 0) /
          allTrades.length
        : 0;

    // Calculate total profit (only positive PnL)
    const totalProfit = allTrades.reduce((sum, trade) => {
      const pnl = parseFloat(trade.realizedPnl.toString());
      return pnl > 0 ? sum + pnl : sum;
    }, 0);

    // Get profit trend (last 30 days vs previous 30 days)
    const last30DaysTrades = await this.tradeRepo
      .createQueryBuilder('trade')
      .where('trade.creatorId = :userId', { userId })
      .andWhere('trade.createdAt >= :thirtyDaysAgo', { thirtyDaysAgo })
      .andWhere('trade.status = :closedStatus', {
        closedStatus: type.status['close'],
      })
      .getMany();

    const previous30DaysTrades = await this.tradeRepo
      .createQueryBuilder('trade')
      .where('trade.creatorId = :userId', { userId })
      .andWhere('trade.createdAt >= :sixtyDaysAgo', { sixtyDaysAgo })
      .andWhere('trade.createdAt < :thirtyDaysAgo', { thirtyDaysAgo })
      .andWhere('trade.status = :closedStatus', {
        closedStatus: type.status['close'],
      })
      .getMany();

    const current30DaysProfit = last30DaysTrades.reduce((sum, trade) => {
      const pnl = parseFloat(trade.realizedPnl.toString());
      return pnl > 0 ? sum + pnl : sum;
    }, 0);

    const previous30DaysProfit = previous30DaysTrades.reduce((sum, trade) => {
      const pnl = parseFloat(trade.realizedPnl.toString());
      return pnl > 0 ? sum + pnl : sum;
    }, 0);

    const percentageChange =
      previous30DaysProfit > 0
        ? ((current30DaysProfit - previous30DaysProfit) /
            previous30DaysProfit) *
          100
        : current30DaysProfit > 0
          ? 100
          : 0;

    // Get number of followers (unique users who copied trades)

    // Get risk level trends
    const results = await this.tradeRepo
      .createQueryBuilder('trade')
      .select('trade.riskLevel', 'riskLevel')
      .addSelect('COUNT(*)', 'count')
      .groupBy('trade.riskLevel')
      .orderBy('count', 'DESC')
      .getRawMany();

    let treadingRisk: type.riskLevel;
    if (results.length === 0) treadingRisk = type.riskLevel['low'];
    treadingRisk = results[0].riskLevel;

    const followers = await this.follower.find({
      where: { followingId: userId },
    });

    return {
      activeTrade: openTrades,
      closedTrade: closedTrades,
      totalPnL,
      winRate: Math.round(winRate * 100) / 100,
      averageROI: Math.round(averageROI * 10000) / 10000,
      currentProfit: totalProfit,
      profitChange: {
        amount: current30DaysProfit,
        percentage: Math.round(percentageChange * 100) / 100,
        isIncreased: percentageChange > 0,
      },
      followers: followers.length,
      riskLevelTrends: treadingRisk,
    };
  }

  async update(
    id: string,
    update: type.updateTrade,
    user: AuthUser,
  ): Promise<type.ITrades | null> {
    //first find the trader
    const trade = await this.tradeRepo.findOne({
      where: { id, creatorId: user.id, status: Not(type.status['close']) },
    });
    if (!trade) {
      throw new NotFoundException('Trade not found');
    }

    // check if the trade as not be copy by anybody
    const ableToEdit = await this.tradeRepo.find({
      where: { identifier: trade.identifier },
    });

    if (ableToEdit.length >= 2) {
      throw new ForbiddenException(
        'Trade cannot be edited after it has been copied by followers',
      );
    }
    const now = new Date();
    const DURATION_MAP = {
      [type.duration['scalp']]: 5 * 60 * 1000,
      [type.duration['intraday']]: 24 * 60 * 60 * 1000,
      [type.duration['swing']]: 7 * 24 * 60 * 60 * 1000,
      [type.duration['position']]: 30 * 24 * 60 * 60 * 1000,
    };

    let tradeStatus: type.status = type.status['draft'];
    // check if trade is a draft before now
    if (!update.isDraft && trade.isDraft) {
      if (update.duration === type.duration['custom']) {
        if (!update.startDate || !update.endDate) {
          throw new ForbiddenException(
            'Custom trade duration must provide startDate and endDate',
          );
        }
        update.startDate = new Date(update.startDate);
        update.expiresAt = new Date(update.endDate);

        const delayStart = update.startDate.getTime() - Date.now();
        const delayEnd = update.expiresAt.getTime() - Date.now();

        update.scheduleStartId = this.tradeJW.scheduleTrade(
          { identifier: trade.identifier, type: 'starting' },
          delayStart,
        );

        update.scheduleEndId = this.tradeJW.scheduleTrade(
          { identifier: trade.identifier, type: 'expiring' },
          delayEnd,
        );
      } else {
        type DurationKey = keyof typeof DURATION_MAP;
        const duration = update.duration ?? trade.duration;
        const ms = DURATION_MAP[duration as DurationKey];
        update.startDate = now;
        update.expiresAt = new Date(now.getTime() + ms);

        const delayEnd = update.expiresAt.getTime() - Date.now();
        update.scheduleEndId = this.tradeJW.scheduleTrade(
          { identifier: trade.identifier, type: 'expiring' },
          delayEnd,
        );
      }

      if (update.isDraft) {
        tradeStatus = type.status['draft'];
      } else if (
        update.duration === type.duration['custom'] &&
        update.startDate > now
      ) {
        tradeStatus = type.status['schedule'];
      } else {
        tradeStatus = type.status['pending'];
      }
    }
    void this.activityFeed.create({
      title: 'Trade Updated',
      message: `Modified ${trade.asset} trade - New Stop Loss: ${trade.stopLoss.toLocaleString()}`,
      userId: user.id,
    });
    await this.tradeRepo.update({ id }, { ...update, status: tradeStatus });
    return { ...trade, ...update };
  }

  async remove(id: string, user: AuthUser) {
    //first find the trader
    const trade = await this.tradeRepo.findOne({
      where: { id, creatorId: user.id },
    });
    if (!trade) {
      throw new NotFoundException('Trade not found');
    }

    if (trade.status === type.status['close']) {
      throw new ForbiddenException('Unable to update trade close');
    }
    // check if the trade as not be copy by anybody
    const ableToEdit = await this.tradeRepo.find({
      where: { identifier: trade.identifier },
    });

    if (ableToEdit.length >= 2) {
      throw new ForbiddenException(
        'Unable to delete, Trade have been copy by followers',
      );
    }

    // allow delete
    return this.tradeRepo.delete(id);
  }

  async sendNotificationJob(dto: type.notifyFollowers) {
    // Get followers
    const followers = await this.follower.find({
      where: { followingId: dto.creatorId },
      select: ['followerId'],
    });
    if (!followers.length)
      return { total: 0, succeeded: 0, failed: 0, failedEmails: [] };

    const userIds = followers.map((f) => f.followerId);

    // Get creator info
    const creator = await this.userRepo.findOne({
      where: { id: dto.creatorId },
      select: ['fullName'],
    });
    if (!creator)
      return { total: 0, succeeded: 0, failed: 0, failedEmails: [] };

    // Get follower user details
    const users = await this.userRepo.find({
      where: { id: In(userIds) },
      select: ['email', 'fullName'],
    });
    if (!users.length) {
      return { total: 0, succeeded: 0, failed: 0, failedEmails: [] };
    }

    // Batch and summary
    const batchSize = 10;
    const total = users.length;
    let succeeded = 0;
    let failed = 0;
    const failedEmails: string[] = [];

    const trade = await this.tradeRepo.findOne({
      where: { id: dto.tradeId },
    });

    if (!trade) {
      return { total: 0, succeeded: 0, failed: 0, failedEmails: [] };
    }

    for (let i = 0; i < total; i += batchSize) {
      const batch = users.slice(i, i + batchSize);

      const results = await Promise.allSettled(
        batch.map((user) =>
          this.mailService.sendMail(
            user.email,
            template.tradeNote,
            `${creator.fullName} just posted a new trade`,
            {
              username: user.fullName,
              proTraderName: creator.fullName,
              symbol: trade.asset,
              direction: trade.orderType,
              price: trade.margin,
              stopLoss: trade.stopLoss,
              takeProfit: trade.takeProfit,
              currentYear: new Date().getFullYear(),
            },
          ),
        ),
      );

      // Update summary counters
      results.forEach((result, idx) => {
        if (result.status === 'fulfilled') succeeded++;
        else {
          failed++;
          failedEmails.push(batch[idx].email);
        }
      });

      if (i + batchSize < total) {
        await sleep(500); // Sleep between batches to manage concurrency
      }
    }
    const summary = { total, succeeded, failed, failedEmails };

    // logger.info('Email job summary:', summary);

    return summary;
  }

  private filter(query: type.findManyTrade) {
    const filter: Record<string, any> = {};

    if (query.creatorId) filter['creatorId'] = query.creatorId;
    if (query.status) filter['status'] = { $eq: query.status };
    if (query.symbol) filter['symbol'] = query.symbol;
    if (query.userId) filter['userId'] = query.userId;
    if (query.type) filter['tradeType'] = { $eq: query.type };
    if (query.asset) filter['asset'] = query.asset;
    if (query.action) filter['action'] = { $eq: query.action };
    if (query.outcome) filter['outcome'] = query.outcome;
    if (query.draft) filter['isDraft'] = { $eq: query.draft };
    if (query.riskLevel) filter['riskLevel'] = { $eq: query.riskLevel };
    if (query.fromDate && query.toDate) {
      filter['createdAt'] = { $between: [query.fromDate, query.toDate] };
    }

    if (query.timeFrame) {
      const currentDate = new Date();
      switch (query.timeFrame) {
        // case 'top7days':
        //   filter['createdAt'] = { $gte: calculateTop7Days(currentDate) };
        //   break;
        case 'last7days':
          filter['createdAt'] = { $gte: this.calculateDaysAgo(currentDate, 7) };
          break;
        case 'last30days':
          filter['createdAt'] = {
            $gte: this.calculateDaysAgo(currentDate, 30),
          };
          break;
        case 'last3months':
          filter['createdAt'] = {
            $gte: this.calculateDaysAgo(currentDate, 90),
          };
          break;
      }
    }

    if (query.roiRange) {
      switch (query.roiRange) {
        case '0-10':
          filter['tradeRoi'] = { $between: [0, 10] };
          break;
        case '10-30':
          filter['tradeRoi'] = { $between: [10, 30] };
          break;
        case '30':
          filter['tradeRoi'] = { $gt: 30 };
          break;
      }
    }

    return filter;
  }

  private calculateDaysAgo(date: Date, days: number): Date {
    const result = new Date(date);
    result.setDate(date.getDate() - days);
    return result;
  }
}
