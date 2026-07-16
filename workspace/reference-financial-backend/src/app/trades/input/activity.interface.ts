import { findMany } from '@app/common';
import { IUser } from '@app/users/interface';

export interface ActivityFeed {
  id: string;
  title: string;
  message: string;
  userId: string;
  user: IUser;
  createdAt: Date;
  updatedAt: Date;
}

export type createActivity = Pick<ActivityFeed, 'title' | 'message' | 'userId'>;

export interface findManyActivity extends findMany {
  userId?: string[];
  title?: string[];
}

export interface profileStats {
  sevenDayRoi: number;
  avgCopierProfit: number;
  riskLevel: number;
  winRate: number;
  user: IUser | null;
  copiers: number;
  follower: number;
  isFollowing: boolean;
}

export interface allTraders extends IUser {
  totalFollowers: number;
  roi: number | null;
  riskScore: number;
  isFollowing: boolean;
}

export interface CopierStats {
  copiers: IUser[];
  totalCopiedUsers: number;
  totalCopiers: number;
}

export interface copierInput {
  traderId: string;
  limit: number;
  page: number;
}

export interface copierBreakdown {
  copiers: {
    user: IUser;
    totalProfit: number;
    totalTrades: number;
    daysCopying: number;
    status: string;
  }[];
  totalCopiedUsers: number;
}

export interface copierMap {
  user: IUser;
  totalProfit: number;
  totalTrades: number;
  firstTradeDate: Date;
  lastTradeDate: Date;
}
