import { AuthUser } from '@app/common';
import { MailService, PaymentService, template } from '@app/services';
import { UsersService } from '@app/users/service';
import { category } from '@app/wallets/input';
import { USDCService } from '@app/wallets/service';
import {
  BadRequestException,
  ForbiddenException,
  forwardRef,
  Inject,
  Injectable,
} from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { OnEvent } from '@nestjs/event-emitter';
import { InjectRepository } from '@nestjs/typeorm';
import { AxiosError } from 'axios';
import Big from 'big.js';
import { Repository } from 'typeorm';
import { Trades } from '../entities';
import { createTrade, duration, outcome, riskLevel, status } from '../input';
import { BybitService } from './bybit.service';
import { TradeJobWorker } from './trade-schedule.service';
import { ActivityService } from './activities.service';

@Injectable()
export class TradeDefineService {
  constructor(
    @InjectRepository(Trades) private readonly tradeRepo: Repository<Trades>,
    private readonly usdcService: USDCService,

    @Inject(forwardRef(() => TradeJobWorker))
    private readonly tradeJW: TradeJobWorker,

    private readonly bybitService: BybitService,
    private readonly userService: UsersService,
    private readonly configService: ConfigService,
    private readonly mailService: MailService,
    private readonly activityFeed: ActivityService,
    private readonly paymentService: PaymentService,
  ) {}

  toUrlParams(data: Record<string, any>): URLSearchParams {
    const searchParams = new URLSearchParams();
    Object.entries(data).forEach(([key, value]) => {
      if (Array.isArray(value)) {
        // eslint-disable-next-line @typescript-eslint/no-unsafe-argument
        value.forEach((v) => searchParams.append(key, v));
      } else if (typeof value === 'boolean') {
        searchParams.append(key, String(value));
      } else if (value !== undefined && value !== null) {
        // eslint-disable-next-line @typescript-eslint/no-unsafe-argument
        searchParams.append(key, value);
      }
      // skip undefined/null
    });
    return searchParams;
  }

  calculateRisk(leverage: number) {
    if (leverage <= 4) return riskLevel.low;
    if (leverage <= 9) return riskLevel.medium;
    return riskLevel.high;
  }

  calculateTradeResults(margin: number, realizedPnL: number) {
    if (!margin || margin <= 0) {
      return { tradeRoi: 0, outcome: outcome.liq };
    }

    const roi = Big(realizedPnL).div(Big(margin)).times(Big(100)).toNumber();

    const tradeOutcome =
      realizedPnL > 0
        ? outcome.win
        : realizedPnL < 0
          ? outcome.loss
          : outcome.liq;

    return { tradeRoi: roi, outcome: tradeOutcome };
  }

  @OnEvent('trade.pnl.realized')
  async fundUsers(data: {
    realizedPnL: number;
    orderId: string;
    orderLinkId: string;
  }) {
    const trade = await this.tradeRepo.findOne({
      where: {
        orderId: data.orderId,
      },
      relations: ['user'],
    });

    if (!trade) return;

    const exitPrices = await this.bybitService.getCurrentPrice(
      trade.symbol,
      'linear',
    );

    const totalCredit = Big(trade.margin).add(Big(data.realizedPnL)).toNumber();

    const calculate = this.calculateTradeResults(
      trade.margin,
      data.realizedPnL,
    );

    // console.log({ calculate, totalCredit, trade, exitPrices });

    if (totalCredit > 0) {
      void this.paymentService.internalCreditUser({
        amount: totalCredit,
        category: category.trade,
        user: trade.user,
      });
    }

    trade.status = status.close;
    trade.exitPrice = exitPrices || 0;
    trade.realizedPnl = data.realizedPnL;
    trade.outcome = calculate.outcome;
    trade.tradeRoi = calculate.tradeRoi;

    void this.activityFeed.create({
      title: 'Trade Closed',
      message: `${trade.asset} trade closed at: ${trade.exitPrice.toLocaleString()} - ${trade.realizedPnl}% P&L`,
      userId: trade.userId,
    });

    this.mailService.sendMail(
      trade.user.email,
      template.tradeClose,
      `${trade.symbol} Trade Closed`,
      {
        fullName: trade.user.username || 'Trader',
      },
    );
    return this.tradeRepo.save(trade);
  }

  async handleTradeRefund(userId: string, amount: string) {
    try {
      // find the receiver wallet address
      const receiver = await this.userService.findOne({ id: userId });
      if (!receiver.data) return;

      const receiverWallet = await this.usdcService.createWalletForUser(
        receiver.data,
      );

      if (!receiverWallet) return;

      const email = this.configService.getOrThrow('ADMIN_EMAIL');
      const findUser = await this.userService.findOne({ email });
      if (!findUser.data) return;

      const user: AuthUser = findUser.data;
      const { balances } = await this.usdcService.userWalletBalance(user);
      if (!balances) throw new ForbiddenException('Insufficient balance');
      const bal = Big(balances[0]?.amount || 0).gt(Big(amount));

      await this.mailService.sendMail(
        this.configService.getOrThrow('ADMIN_EMAIL'),
        template.bybit,
        'Circle Payment Process Failed - Insufficient Balance',
        { accountName: 'Circle' },
      );
      if (!bal) throw new ForbiddenException('Insufficient balance');

      return this.usdcService.onChainTransfer(
        String(amount),
        receiverWallet.address,
        'LOW',
        user,
      );
    } catch (error) {
      if (error instanceof AxiosError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  handleTraderDuration(payload: createTrade, identifier: string) {
    const DURATION_MAP = {
      [duration.scalp]: 5 * 60 * 1000,
      [duration.intraday]: 24 * 60 * 60 * 1000,
      [duration.swing]: 7 * 24 * 60 * 60 * 1000,
      [duration.position]: 30 * 24 * 60 * 60 * 1000,
      [duration.custom]: '',
    };

    if (payload.duration === duration.custom) {
      if (!payload.startDate || !payload.expiresAt) {
        throw new ForbiddenException(
          'Custom trade duration must provide startDate and endDate',
        );
      }

      payload.startDate = new Date(payload.startDate);
      payload.expiresAt = new Date(payload.expiresAt);

      const delayStart = payload.startDate.getTime() - Date.now();
      const delayEnd = payload.expiresAt.getTime() - Date.now();

      if (!payload.isDraft) {
        payload.scheduleStartId = this.tradeJW.scheduleTrade(
          { identifier, type: 'starting' },
          delayStart,
        );

        payload.scheduleEndId = this.tradeJW.scheduleTrade(
          { identifier, type: 'expiring' },
          delayEnd,
        );
      }
    } else {
      const ms = DURATION_MAP[payload.duration];
      payload.startDate = new Date();
      payload.expiresAt = new Date(new Date().getTime() + ms);

      const delayEnd = payload.expiresAt.getTime() - Date.now();
      if (!payload.isDraft) {
        payload.scheduleEndId = this.tradeJW.scheduleTrade(
          { identifier, type: 'expiring' },
          delayEnd,
        );
      }
    }

    return payload;
  }
}
