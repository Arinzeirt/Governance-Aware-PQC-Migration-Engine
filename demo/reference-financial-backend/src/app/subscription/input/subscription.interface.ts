import { IUser } from '@app/users/interface';

export enum SubscriptionStatus {
  active = 'active',
  canceled = 'canceled',
  expired = 'expired',
  past_due = 'past_due',
  pending = 'pending',
}

export enum PlanName {
  free = 'Free',
  premium = 'Premium',
}

export enum Period {
  week = 'Weekly',
  month = 'Monthly',
  quarter = 'Quarterly',
  year = 'Yearly',
}

export interface SubPlan {
  id: string;
  name: PlanName;
  period: Period;
  features?: string[];
  price: number;
  createdAt: Date;
  updatedAt: Date;
}

export interface createSubPlan
  extends Omit<SubPlan, 'id' | 'createdAt' | 'updatedAt'> {}

export interface Subscriptions {
  id: string;
  user: IUser;
  plan: SubPlan;
  status: SubscriptionStatus;
  createdAt: Date;
  updatedAt: Date;
}

export interface subscribe {
  planId: string;
}
