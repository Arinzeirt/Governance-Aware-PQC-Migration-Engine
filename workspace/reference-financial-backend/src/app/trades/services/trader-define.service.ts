import { Injectable } from '@nestjs/common';
import { addDays, format, isWithinInterval, subDays } from 'date-fns';
import { Trades } from '../entities';
import { DrawdownPoint, findManyActivity, PerfPoint, Period } from '../input';

@Injectable()
export class TraderDefineService {
  constructor() {}

  buildPerformanceCurve(trades: Trades[], periodDays: number): PerfPoint[] {
    const end = new Date();
    const start = subDays(end, periodDays - 1);

    // Group trades by date
    const tradesByDate: Record<string, number> = {};
    trades
      .filter((trade) =>
        isWithinInterval(new Date(trade.updatedAt), { start, end }),
      )
      .forEach((trade) => {
        const d = format(new Date(trade.updatedAt), 'yyyy-MM-dd');
        tradesByDate[d] = (tradesByDate[d] || 0) + (trade.realizedPnl || 0);
      });

    // Running cumulative PnL per day
    const dateArr = this.getDateArray(start, end);
    let cumulative = 0;
    const result: PerfPoint[] = [];
    dateArr.forEach((dateStr) => {
      if (tradesByDate[dateStr]) cumulative += tradesByDate[dateStr];
      result.push({
        date: dateStr,
        cumulative,
      });
    });
    return result;
  }

  buildDrawdownCurve(trades: Trades[], periodDays: number): DrawdownPoint[] {
    // 1. get desired window
    const end = new Date();
    const start = subDays(end, periodDays - 1); // ensures periodDays total

    // 2. group trades by date
    const tradesByDate: Record<string, number> = {};
    trades
      .filter((trade) =>
        isWithinInterval(new Date(trade.updatedAt), { start, end }),
      )
      .forEach((trade) => {
        const d = format(new Date(trade.updatedAt), 'yyyy-MM-dd');
        tradesByDate[d] = (tradesByDate[d] || 0) + (trade.realizedPnl || 0);
      });

    // 3. create a running curve from start to end (fills missing days)
    const dateArr = this.getDateArray(start, end);
    let cumulative = 0;
    let peak = 0;
    const result: DrawdownPoint[] = [];
    dateArr.forEach((dateStr) => {
      // if no trade, PnL stays flat
      if (tradesByDate[dateStr]) cumulative += tradesByDate[dateStr];
      // drawdown logic
      if (cumulative > peak) peak = cumulative;
      const drawdown = cumulative - peak;
      result.push({
        date: dateStr,
        drawdown, // negative or zero
      });
    });
    return result;
  }

  getDateArray(start: Date, end: Date): string[] {
    const dates = [];
    let current = start;
    while (current <= end) {
      dates.push(format(current, 'yyyy-MM-dd'));
      current = addDays(current, 1);
    }
    return dates;
  }

  filterTradesByPeriod(trades: Trades[], period: Period) {
    const now = new Date();
    let start: Date;
    switch (period) {
      case 'daily':
        start = subDays(now, 1);
        break;
      case '7D':
        start = subDays(now, 7);
        break;
      case '30D':
        start = subDays(now, 30);
        break;
      case '90D':
        start = subDays(now, 90);
        break;
      case '1YR':
        start = subDays(now, 365);
        break;
      case '2YR':
        start = subDays(now, 730);
        break;
      default:
        start = subDays(now, 1);
    }

    return trades.filter((trade) =>
      isWithinInterval(trade.updatedAt, {
        start,
        end: now,
      }),
    );
  }

  calculateTraderMetrics(trades: Trades[]) {
    // 1. Total Trades
    const totalTrades = trades.length;

    // 2. Win Rate (%)
    const wins = trades.filter((t) => (t.realizedPnl || 0) > 0).length;
    const winRate = (wins / totalTrades) * 100;

    // 3. Average Trade Duration
    const durations = trades
      .filter((t) => t.startDate && t.expiresAt)
      .map((t) => {
        const start = new Date(t.startDate).getTime();
        const end = new Date(t.expiresAt).getTime();
        return (end - start) / (1000 * 60 * 60); // convert to hours
      });
    const AvgTradeDuration = durations.length
      ? durations.reduce((a, b) => a + b, 0) / durations.length
      : 0;

    // 4. Biggest Win
    const biggestWin = Math.max(...trades.map((t) => t.realizedPnl || 0), 0);

    // 5. Biggest Loss
    const biggestLoss = Math.abs(
      Math.min(...trades.map((t) => t.realizedPnl || 0), 0),
    );

    // 6. Risk Level (average riskLevel from all trades)
    const riskLevelMap: Record<string, number> = {
      Low: 1,
      Medium: 2,
      High: 3,
    };
    const riskLevels = trades
      .filter((t) => t.riskLevel)
      .map((t) => riskLevelMap[t.riskLevel] || 0);
    const riskLevel = riskLevels.length
      ? riskLevels.reduce((a, b) => a + b, 0) / riskLevels.length
      : 0;

    return {
      totalTrades,
      winRate: Number(winRate.toFixed(2)),
      AvgTradeDuration: Number(AvgTradeDuration.toFixed(2)),
      biggestWin: Number(biggestWin.toFixed(2)),
      riskLevel: Number(riskLevel.toFixed(2)),
      biggestLoss: Number(biggestLoss.toFixed(2)),
    };
  }

  filter(query: findManyActivity) {
    const filter: Record<string, any> = {};
    if (query.userId) filter['userId'] = query.userId;
    if (query.title) filter['title'] = query.title;
    return filter;
  }

  getTotalRoiPercentage(trades: Trades[]): number {
    if (!trades.length) return 0;
    const totalRoi = trades.reduce(
      (sum, trade) => sum + (trade.tradeRoi || 0),
      0,
    );
    const avgRoi = totalRoi / trades.length;

    return Number(avgRoi.toFixed(2));
  }

  getRoiByMonth(trades: Trades[], period: Period): Record<string, number> {
    // Group trades by month
    const roiByMonth: Record<string, { totalRoi: number; count: number }> = {};
    const filtered = this.filterTradesByPeriod(trades, period);
    filtered.forEach((trade) => {
      const monthKey = format(new Date(trade.updatedAt), 'MMM'); // 'Jan', 'Feb', etc.
      if (!roiByMonth[monthKey]) {
        roiByMonth[monthKey] = { totalRoi: 0, count: 0 };
      }
      roiByMonth[monthKey].totalRoi += trade.tradeRoi || 0;
      roiByMonth[monthKey].count += 1;
    });

    // Convert to average ROI percentage per month
    const result: Record<string, number> = {};
    for (const [month, data] of Object.entries(roiByMonth)) {
      result[month] = Number((data.totalRoi / data.count).toFixed(2));
    }
    return result;
  }

  get7DayRoiPercentage(trades: Trades[]): number {
    const filtered = this.filterTradesByPeriod(trades, '7D');
    return this.getTotalRoiPercentage(filtered);
  }

  get7DayRiskLevel(trades: Trades[]): number {
    const filtered = this.filterTradesByPeriod(trades, '7D');
    const riskLevelMap: Record<string, number> = {
      Low: 1,
      Medium: 2,
      High: 3,
    };
    const riskLevels = filtered
      .filter((t) => t.riskLevel)
      .map((t) => riskLevelMap[t.riskLevel] || 0);
    const avgRiskLevel = riskLevels.length
      ? riskLevels.reduce((a, b) => a + b, 0) / riskLevels.length
      : 0;

    return Number(avgRiskLevel.toFixed(2));
  }

  getLossRecord(trades: Trades[]): {
    totalLosses: number;
    lossCount: number;
    avgLoss: number;
  } {
    const losingTrades = trades.filter((t) => (t.realizedPnl || 0) < 0);
    const totalLosses = losingTrades.reduce(
      (sum, t) => sum + Math.abs(t.realizedPnl || 0),
      0,
    );
    const avgLoss = losingTrades.length ? totalLosses / losingTrades.length : 0;

    return {
      totalLosses: Number(totalLosses.toFixed(2)),
      lossCount: losingTrades.length,
      avgLoss: Number(avgLoss.toFixed(2)),
    };
  }

  getWinRecord(trades: Trades[]): {
    totalWins: number;
    winCount: number;
    avgWin: number;
  } {
    const winningTrades = trades.filter((t) => (t.realizedPnl || 0) > 0);
    const totalWins = winningTrades.reduce(
      (sum, t) => sum + (t.realizedPnl || 0),
      0,
    );
    const avgWin = winningTrades.length ? totalWins / winningTrades.length : 0;

    return {
      totalWins: Number(totalWins.toFixed(2)),
      winCount: winningTrades.length,
      avgWin: Number(avgWin.toFixed(2)),
    };
  }
}
