import { AuthUser } from '@app/common';
import { Injectable, InternalServerErrorException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository, TypeORMError } from 'typeorm';
import { Trades } from '../entities';
import {
  copierBreakdown,
  copierInput,
  copierMap,
  outcome,
  Period,
  status,
  type,
} from '../input';
import { TraderDefineService } from './trader-define.service';

@Injectable()
export class CopierService {
  constructor(
    @InjectRepository(Trades) private readonly tradeRepo: Repository<Trades>,
    private readonly tdService: TraderDefineService,
  ) {}

  async getUserAssetDashboard(user: AuthUser) {
    try {
      const trades = await this.tradeRepo.find({ where: { userId: user.id } });
      if (!trades.length) {
        return {
          roi: {
            current: 0,
            percent: 0,
            increase: false,
          },
          winRate: {
            current: 0,
            percent: 0,
            increase: false,
          },
          activeTrade: {
            current: 0,
            inProfit: 0,
            increase: false,
          },
          totalCopy: {
            current: 0,
            percent: 0,
            increase: false,
          },
        };
      }

      const now = new Date();
      const sevenDaysAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
      const fourteenDaysAgo = new Date(
        now.getTime() - 14 * 24 * 60 * 60 * 1000,
      );

      const completedTrades = trades.filter(
        (trade) => trade.outcome && trade.status === status.close,
      );

      const activeTrade = trades.filter((trade) =>
        [status.pending, status.open].includes(trade.status),
      );

      // ROI: current total ROI and 7-day change vs previous 7 days
      const roiCurrent = this.tdService.getTotalRoiPercentage(trades);

      const last7DaysTrades = trades.filter(
        (t) => new Date(t.createdAt) >= sevenDaysAgo,
      );
      const prev7DaysTrades = trades.filter((t) => {
        const created = new Date(t.createdAt);
        return created >= fourteenDaysAgo && created < sevenDaysAgo;
      });

      const roiLast7Days =
        last7DaysTrades.length > 0
          ? this.tdService.getTotalRoiPercentage(last7DaysTrades)
          : 0;

      const roiPrev7Days =
        prev7DaysTrades.length > 0
          ? this.tdService.getTotalRoiPercentage(prev7DaysTrades)
          : 0;

      const roiPercentChange =
        roiPrev7Days !== 0
          ? ((roiLast7Days - roiPrev7Days) / Math.abs(roiPrev7Days)) * 100
          : 0;

      const roiIncrease = roiLast7Days >= roiPrev7Days;

      const roi = {
        current: Number(roiCurrent.toFixed(2)),
        percent: Number(roiPercentChange.toFixed(2)),
        increase: roiIncrease,
      };

      // Win rate: based on last 10 completed trades compared to previous 10
      const completedSorted = [...completedTrades].sort(
        (a, b) =>
          new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime(),
      );

      const last10Completed = completedSorted.slice(-10);
      const prev10Completed =
        completedSorted.length > 10
          ? completedSorted.slice(
              Math.max(0, completedSorted.length - 20),
              completedSorted.length - 10,
            )
          : [];

      const last10Wins = last10Completed.filter(
        (t) => t.outcome === outcome.win,
      );

      const prev10Wins = prev10Completed.filter(
        (t) => t.outcome === outcome.win,
      );

      const winRateCurrent =
        last10Completed.length > 0
          ? (last10Wins.length / last10Completed.length) * 100
          : 0;

      const winRatePrev =
        prev10Completed.length > 0
          ? (prev10Wins.length / prev10Completed.length) * 100
          : 0;

      const winRatePercentChange =
        winRatePrev !== 0
          ? ((winRateCurrent - winRatePrev) / Math.abs(winRatePrev)) * 100
          : 0;

      const winRateIncrease = winRateCurrent >= winRatePrev;

      const winRate = {
        current: Number(winRateCurrent.toFixed(2)),
        percent: Number(winRatePercentChange.toFixed(2)),
        increase: winRateIncrease,
      };

      // Active trades: current active count, in-profit count and ratio-based increase flag
      const inProfitActive = activeTrade.filter((t) => {
        if (t.entryPrice == null || t.currentPrice == null) return false;
        if (t.action === 'Buy') {
          return t.currentPrice > t.entryPrice;
        }
        return t.currentPrice < t.entryPrice;
      });

      const activeCurrent = activeTrade.length;
      const inProfitCount = inProfitActive.length;

      // Mark as increase if at least half of active trades are in profit
      const activeIncrease =
        activeCurrent > 0
          ? inProfitCount >= Math.ceil(activeCurrent / 2)
          : false;

      const activeTradeStat = {
        current: activeCurrent,
        inProfit: inProfitCount,
        increase: activeIncrease,
      };

      // Total copied trades: this week vs last week by createdAt and tradeType = copy
      const copyTrades = trades.filter((t) => t.tradeType === type.copy);

      const thisWeekCopies = copyTrades.filter(
        (t) => new Date(t.createdAt) >= sevenDaysAgo,
      ).length;

      const lastWeekCopies = copyTrades.filter((t) => {
        const created = new Date(t.createdAt);
        return created >= fourteenDaysAgo && created < sevenDaysAgo;
      }).length;

      const copyPercentChange =
        lastWeekCopies !== 0
          ? ((thisWeekCopies - lastWeekCopies) / Math.abs(lastWeekCopies)) * 100
          : 0;

      const copyIncrease = thisWeekCopies >= lastWeekCopies;

      const totalCopy = {
        current: thisWeekCopies,
        percent: Number(copyPercentChange.toFixed(2)),
        increase: copyIncrease,
      };

      return {
        roi,
        winRate,
        activeTrade: activeTradeStat,
        totalCopy,
      };
    } catch (error) {
      if (error instanceof TypeORMError) {
        throw new InternalServerErrorException();
      }
      throw error;
    }
  }

  async performanceBreakdown(range: Period, user: AuthUser) {
    try {
      const trades = await this.tradeRepo.find({ where: { userId: user.id } });
      if (!trades.length) {
        return {
          riskLevel: 0,
          winningTrades: 0,
          roi: 0,
          losingTrades: 0,
          drawdown: 0,
        };
      }
      const filtered = this.tdService.filterTradesByPeriod(trades, range);

      const roi = this.tdService.getTotalRoiPercentage(filtered);
      const riskLevelMap: Record<string, number> = {
        Low: 1,
        Medium: 2,
        High: 3,
      };

      const riskLevels = filtered
        .filter((t) => t.riskLevel)
        .map((t) => riskLevelMap[t.riskLevel] || 0);

      const riskLevel = riskLevels.length
        ? riskLevels.reduce((a, b) => a + b, 0) / riskLevels.length
        : 0;

      const winningTrades = filtered.filter(
        (trade) => trade.outcome === outcome.win,
      );

      const losingTrades = filtered.filter(
        (trade) => trade.outcome === outcome.loss,
      );

      const drawdown = this.getMinimumDrawdown(filtered);

      return {
        riskLevel,
        winningTrades: winningTrades.length,
        roi,
        losingTrades: losingTrades.length,
        drawdown,
      };
    } catch (error) {
      if (error instanceof TypeORMError) {
        throw new InternalServerErrorException();
      }
      throw error;
    }
  }

  async copierBreakdown(query: copierInput): Promise<copierBreakdown> {
    const trades = await this.tradeRepo.find({
      where: { creatorId: query.traderId },
      relations: ['user'],
      order: {
        createdAt: 'DESC',
      },
    });

    if (!trades.length) {
      return {
        copiers: [],
        totalCopiedUsers: 0,
      };
    }

    const copiersMap = new Map<string, copierMap>();
    trades.forEach((trade) => {
      // Only include trades where the user is NOT the creator (these are copiers)
      if (trade.userId === trade.creatorId) return;

      const copierId = trade.userId;
      let stats = copiersMap.get(copierId);

      if (!stats) {
        stats = {
          user: trade.user,
          totalProfit: 0,
          totalTrades: 0,
          firstTradeDate: trade.startDate,
          lastTradeDate: trade.startDate,
        };
        copiersMap.set(copierId, stats);
      }

      stats.totalProfit += trade.realizedPnl || 0;
      stats.totalTrades += 1;

      const tradeDate = new Date(trade.startDate);
      if (tradeDate < new Date(stats.firstTradeDate)) {
        stats.firstTradeDate = trade.startDate;
      }
      if (tradeDate > new Date(stats.lastTradeDate)) {
        stats.lastTradeDate = trade.startDate;
      }
    });

    const now = new Date();
    const copiers = Array.from(copiersMap.values()).map((stats) => {
      const firstDate = new Date(stats.firstTradeDate).getTime();
      const lastDate = new Date(stats.lastTradeDate).getTime();
      const daysCopying = Math.max(
        1,
        Math.ceil((lastDate - firstDate) / (1000 * 60 * 60 * 24)),
      );

      const diffMs = now.getTime() - lastDate;
      const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

      return {
        user: stats.user,
        totalProfit: Number(stats.totalProfit.toFixed(2)),
        totalTrades: stats.totalTrades,
        daysCopying,
        status: diffDays > 30 ? 'Stopped' : 'Active',
      };
    });

    const skip = (query.page - 1) * query.limit;
    const take = query.limit;

    const paginatedCopiers = copiers.slice(skip, skip + take);
    return {
      copiers: paginatedCopiers,
      totalCopiedUsers: copiers.length,
    };
  }

  private getMinimumDrawdown(trades: Trades[]): number {
    if (!trades || trades.length === 0) return 0;

    const ordered = trades
      .slice()
      .sort(
        (a, b) =>
          new Date(a.updatedAt).getTime() - new Date(b.updatedAt).getTime(),
      );

    let cumulative = 0;
    let peak = Number.NEGATIVE_INFINITY;
    let maxDdPct = 0;
    const history: number[] = [];

    for (const t of ordered) {
      cumulative += t.realizedPnl || 0;
      history.push(cumulative);
      if (cumulative > peak) peak = cumulative;
      const dd = peak - cumulative; // positive drawdown amount
      if (dd > 0 && peak !== 0) {
        const pct = (dd / Math.abs(peak)) * 100;
        if (pct > maxDdPct) maxDdPct = pct;
      } else if (dd > 0 && peak === 0) {
        // peak 0 -> treat drawdown as 100% of zero baseline (use 100 to indicate full drop)
        if (100 > maxDdPct) maxDdPct = 100;
      }
    }

    // net change percent from first to last cumulative (signed)
    const first = history[0] ?? 0;
    const last = history[history.length - 1] ?? 0;
    const netChangePercent =
      Math.abs(first) > 0
        ? ((last - first) / Math.abs(first)) * 100
        : last === 0
          ? 0
          : Math.sign(last) * 100;

    // prefer drawdown when it exists, returned as negative; otherwise return net change (signed)
    if (maxDdPct > 0) return Number((-maxDdPct).toFixed(2));
    return Number(netChangePercent.toFixed(2));
  }
}
