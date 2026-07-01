import { IUser } from '@app/users/interface';
import { SubPlan, SubscriptionStatus } from './subscription.interface';
import { findMany, findOne } from '@app/common';

export interface IHistory {
  id: string;
  user: IUser;
  price: number;
  plan: SubPlan;
  paymentId?: string;
  startingDate: Date;
  expiringDate: Date;
  changeReason: string;
  status: SubscriptionStatus;
  scheduleId?: number;
  metadata: Record<string, any>;
  createdAt: Date;
  updatedAt: Date;
}

export type subHistory = Omit<IHistory, 'id' | 'createdAt' | 'updatedAt'>;

export interface findManySubHistory extends findMany {
  user?: string[];
  plan?: string[];
  paymentId?: string[];
  startingDate?: Date[];
  expiringDate?: Date[];
}

export interface findOneSubHistory extends findOne {
  userId?: string;
  planId?: string;
  paymentId?: string;
  user?: { id: string };
  plan?: { id: string };
}
