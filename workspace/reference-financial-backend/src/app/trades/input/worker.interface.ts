import { Job as plainJob } from 'plainjob';

export interface scheduleTrade {
  identifier: string;
  type: 'starting' | 'expiring';
}

export interface copyTraders {
  tradeId: string;
  creatorId: string;
}

export type traders = plainJob & {
  data: copyTraders;
};

export interface placeTrade {
  tradeId: string;
  fundId: string;
}

export type placeTradeJob = plainJob & {
  data: placeTrade;
};

export interface topPairs {
  asset: string;
  symbol: string;
  tradeCount: number;
  totalRoiPercentage: number;
  totalPnl: number;
  winCount: number;
  lossCount: number;
}

export interface refundTradePayment {
  userId: string;
  amount: string;
}

export type refundTradePaymentJob = plainJob & {
  data: refundTradePayment;
};
