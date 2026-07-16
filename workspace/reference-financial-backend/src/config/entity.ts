import {
  Badge,
  GameProgress,
  GamingOnboarding,
  UserBadge,
} from '@app/gamified/entities';
import { Referral, ReferralRewardSetting } from '@app/referral/entities';
import {
  SubPlans,
  Subscription,
  SubscriptionHistory,
} from '@app/subscription/entities';
import {
  CopySettingEntity,
  FollowTraders,
  TradeActivityFeeds,
  Trades,
} from '@app/trades/entities';
import {
  Privileges,
  Protrader,
  RoleModel,
  UserActivity,
} from '@app/users/entity';
import { User } from '@app/users/entity/user.entity';
import { BillTnx } from '@app/utilities/entities';
import {
  Beneficiary,
  CryptoAccounts,
  FiatAccount,
  Transaction,
  Wallets,
  WalletSet,
} from '@app/wallets/entities';
import { WebHookLog } from '@app/webhooks/entity';
import { BlogManager } from 'src/app/blog-manager/entities/blog-manager.entity';
import { EmailCenter, WaitList } from 'src/app/email-center/entities';
import { LearningHub } from 'src/app/learninghub/entities/learninghub.entity';

export const Entity = [
  BlogManager,
  EmailCenter,
  LearningHub,
  User,
  Protrader,
  GameProgress,
  GamingOnboarding,
  WaitList,
  RoleModel,
  Privileges,
  Badge,
  UserBadge,
  Trades,
  TradeActivityFeeds,
  FollowTraders,
  Transaction,
  Wallets,
  FiatAccount,
  CryptoAccounts,
  Referral,
  ReferralRewardSetting,
  Subscription,
  SubscriptionHistory,
  SubPlans,
  Beneficiary,
  WalletSet,
  WebHookLog,
  UserActivity,
  BillTnx,
  CopySettingEntity,
];
