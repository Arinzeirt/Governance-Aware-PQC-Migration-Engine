import {
  forwardRef,
  Inject,
  Injectable,
  InternalServerErrorException,
} from '@nestjs/common';
import { outcome, Period, profileStats, status, topPairs } from '../input';
import { TraderDefineService } from './trader-define.service';
import { InjectRepository } from '@nestjs/typeorm';
import { FollowTraders, Trades } from '../entities';
import { Repository, TypeORMError } from 'typeorm';
import { UsersService } from '@app/users/service';
import { AuthUser } from '@app/common';

@Injectable()
export class ProTradePerformance {
  constructor(
    @InjectRepository(Trades) private readonly tradeRepo: Repository<Trades>,
    @Inject(forwardRef(() => UsersService))
    private readonly userService: UsersService,
    @InjectRepository(FollowTraders)
    private readonly followTrade: Repository<FollowTraders>,
    private readonly tdService: TraderDefineService,
  ) {}

  async tradeProfileStats(
    traderId: string,
    iuser: AuthUser,
  ): Promise<profileStats> {
    const baseQuery = this.tradeRepo
      .createQueryBuilder('trade')
      .where('trade.creatorId = :userId', { userId: traderId });

    // Get all trades for calculations
    const [allTrades, copiedTrades, user, follower, isFollowing] =
      await Promise.all([
        baseQuery.clone().getMany(),
        this.tradeRepo
          .createQueryBuilder('trade')
          .where('trade.creatorId != trade.userId')
          .andWhere('trade.creatorId = :traderId', { traderId })
          .getMany(),
        this.userService.findOne({ id: traderId }),
        this.followTrade.find({ where: { followingId: traderId } }),
        this.followTrade.findOne({
          where: {
            followerId: iuser.id,
            followingId: traderId,
          },
        }),
      ]);

    if (!allTrades.length) {
      return {
        winRate: 0,
        sevenDayRoi: 0,
        avgCopierProfit: 0,
        riskLevel: 0,
        user: user.data,
        copiers: 0,
        follower: follower.length ?? 0,
        isFollowing: !!isFollowing,
      };
    }
    const sevenDayRoi = this.tdService.get7DayRoiPercentage(allTrades);

    let avgCopierProfit = 0;
    if (copiedTrades.length > 0) {
      const totalCopierProfit = copiedTrades.reduce(
        (sum, trade) => sum + (trade.realizedPnl || 0),
        0,
      );
      avgCopierProfit = totalCopierProfit / copiedTrades.length;
    }

    const riskLevelMap: Record<string, number> = {
      Low: 1,
      Medium: 2,
      High: 3,
    };

    const riskLevels = allTrades
      .filter((t) => t.riskLevel)
      .map((t) => riskLevelMap[t.riskLevel] || 0);

    const riskLevel = riskLevels.length
      ? riskLevels.reduce((a, b) => a + b, 0) / riskLevels.length
      : 0;

    const completedTrades = allTrades.filter(
      (trade) => trade.outcome && trade.status === status.close,
    );

    const winningTrades = allTrades.filter(
      (trade) => trade.outcome === outcome.win,
    );

    const winRate =
      completedTrades.length > 0
        ? (winningTrades.length / completedTrades.length) * 100
        : 0;

    return {
      winRate,
      sevenDayRoi: Number(sevenDayRoi.toFixed(2)),
      avgCopierProfit: Number(avgCopierProfit.toFixed(2)),
      riskLevel: Number(riskLevel.toFixed(2)),
      copiers: copiedTrades.length || 0,
      user: user.data,
      follower: follower.length ?? 0,
      isFollowing: !!isFollowing,
    };
  }

  async profitPerformance(period: Period, userId: string) {
    const trades = await this.tradeRepo.find({ where: { userId } });

    if (!trades.length) {
      return {
        totalTrades: 0,
        winRate: 0,
        AvgTradeDuration: 0,
        biggestWin: 0,
        riskLevel: 0,
        biggestLoss: 0,
      };
    }

    const filtered = this.tdService.filterTradesByPeriod(trades, period);
    return this.tdService.calculateTraderMetrics(filtered);
  }

  async drawdownCurve(days: number, userId: string) {
    const trades = await this.tradeRepo.find({ where: { userId } });
    return this.tdService.buildDrawdownCurve(trades, days);
  }

  async performanceCurve(days: number, userId: string) {
    const trades = await this.tradeRepo.find({ where: { userId } });
    return this.tdService.buildPerformanceCurve(trades, days);
  }

  async graph(period: Period, userId: string) {
    const trades = await this.tradeRepo.find({
      where: { creatorId: userId },
    });

    if (!trades.length) {
      return {
        totalRoiPercentage: 0,
        roiByMonth: 0,
        sevenDayRoi: 0,
        sevenDayRiskLevel: 0,
        lossRecord: 0,
        winRecord: 0,
      };
    }

    const filtered = this.tdService.filterTradesByPeriod(trades, period);

    return {
      totalRoiPercentage: this.tdService.getTotalRoiPercentage(filtered),
      roiByMonth: this.tdService.getRoiByMonth(trades, period),
      sevenDayRoi: this.tdService.get7DayRoiPercentage(trades),
      sevenDayRiskLevel: this.tdService.get7DayRiskLevel(trades),
      lossRecord: this.tdService.getLossRecord(filtered),
      winRecord: this.tdService.getWinRecord(filtered),
    };
  }

  async getAssetPerformance(userId: string): Promise<topPairs[]> {
    const trades = await this.tradeRepo.find({
      where: { creatorId: userId },
    });

    if (!trades.length) return [];

    // Group trades by asset
    const assetMap = new Map<string, { trades: Trades[] }>();

    trades.forEach((trade) => {
      const key = `${trade.asset}/${trade.symbol}`;
      if (!assetMap.has(key)) {
        assetMap.set(key, { trades: [] });
      }
      assetMap.get(key)!.trades.push(trade);
    });

    // Calculate stats for each asset
    const result: Array<topPairs> = [];
    assetMap.forEach((data, key) => {
      const [asset, symbol] = key.split('/');
      const assetTrades = data.trades;

      // Total ROI percentage
      const totalRoi = assetTrades.reduce(
        (sum, trade) => sum + (trade.tradeRoi || 0),
        0,
      );
      const avgRoiPercentage =
        assetTrades.length > 0 ? totalRoi / assetTrades.length : 0;

      // Total PnL
      const totalPnl = assetTrades.reduce(
        (sum, trade) => sum + (trade.realizedPnl || 0),
        0,
      );

      // Win/Loss count
      const winCount = assetTrades.filter(
        (t) => (t.realizedPnl || 0) > 0,
      ).length;
      const lossCount = assetTrades.filter(
        (t) => (t.realizedPnl || 0) < 0,
      ).length;

      result.push({
        asset,
        symbol,
        tradeCount: assetTrades.length,
        totalRoiPercentage: Number(avgRoiPercentage.toFixed(2)),
        totalPnl: Number(totalPnl.toFixed(2)),
        winCount,
        lossCount,
      });
    });

    // Sort by trade count (descending)
    return result.sort((a, b) => b.tradeCount - a.tradeCount);
  }

  async copierPerformance(period: Period, userId: string) {
    try {
      const copierTrades = await this.tradeRepo.find({
        where: { creatorId: userId },
      });

      if (!copierTrades.length) {
        return {
          totalCopiers: 0,
          profitableCopiersPercent: 0,
          avgCopierProfit: 0,
          avgHoldingTimeHours: 0,
          maxGain: 0,
          maxLoss: 0,
        };
      }

      const filtered = this.tdService.filterTradesByPeriod(
        copierTrades,
        period,
      );

      const filteredCopierTrades = filtered.filter(
        (t) => t.userId && t.userId !== t.creatorId,
      );

      if (!filteredCopierTrades.length) {
        return {
          totalCopiers: 0,
          profitableCopiersPercent: 0,
          avgCopierProfit: 0,
          avgHoldingTimeHours: 0,
          maxGain: 0,
          maxLoss: 0,
        };
      }

      // Group by copier userId
      const byCopier = new Map<
        string,
        { trades: Trades[]; totalPnl: number }
      >();

      filteredCopierTrades.forEach((trade) => {
        const key = trade.userId;
        if (!byCopier.has(key)) {
          byCopier.set(key, { trades: [], totalPnl: 0 });
        }
        const entry = byCopier.get(key)!;
        entry.trades.push(trade);
        entry.totalPnl += trade.realizedPnl || 0;
      });

      const totalCopiers = byCopier.size;

      // Profitable copiers: copiers whose cumulative PnL > 0
      let profitableCopiers = 0;
      let totalProfitAcrossCopiers = 0;
      let totalHoldingHours = 0;
      let holdingSamples = 0;

      let maxGain = Number.NEGATIVE_INFINITY;
      let maxLoss = Number.POSITIVE_INFINITY;

      byCopier.forEach((entry) => {
        const { trades, totalPnl } = entry;
        if (totalPnl > 0) {
          profitableCopiers += 1;
        }
        totalProfitAcrossCopiers += totalPnl;

        // Holding time per trade: from startDate to expiresAt (or updatedAt as fallback)
        trades.forEach((t) => {
          const start = t.startDate ? new Date(t.startDate).getTime() : null;
          const endSource = t.expiresAt || t.updatedAt;
          const end = endSource ? new Date(endSource).getTime() : null;
          if (start && end && end > start) {
            const hours = (end - start) / (1000 * 60 * 60);
            totalHoldingHours += hours;
            holdingSamples += 1;
          }

          const pnl = t.realizedPnl || 0;
          if (pnl > maxGain) maxGain = pnl;
          if (pnl < maxLoss) maxLoss = pnl;
        });
      });

      const profitableCopiersPercent =
        totalCopiers > 0 ? (profitableCopiers / totalCopiers) * 100 : 0;

      const avgCopierProfit =
        totalCopiers > 0 ? totalProfitAcrossCopiers / totalCopiers : 0;

      const avgHoldingTimeHours =
        holdingSamples > 0 ? totalHoldingHours / holdingSamples : 0;

      const safeMaxGain = maxGain === Number.NEGATIVE_INFINITY ? 0 : maxGain;
      const safeMaxLoss =
        maxLoss === Number.POSITIVE_INFINITY ? 0 : Math.abs(maxLoss);

      return {
        totalCopiers,
        profitableCopiersPercent: Number(profitableCopiersPercent.toFixed(2)),
        avgCopierProfit: Number(avgCopierProfit.toFixed(2)),
        avgHoldingTimeHours: Number(avgHoldingTimeHours.toFixed(2)),
        maxGain: Number(safeMaxGain.toFixed(2)),
        maxLoss: Number(safeMaxLoss.toFixed(2)),
      };
    } catch (error) {
      if (error instanceof TypeORMError) {
        throw new InternalServerErrorException();
      }
      throw error;
    }
  }
}
