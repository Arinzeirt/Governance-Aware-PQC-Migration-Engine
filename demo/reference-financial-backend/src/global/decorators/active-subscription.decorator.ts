import { SetMetadata } from '@nestjs/common';

export const ACTIVE_SUBSCRIPTION_KEY = 'activeSubscription';
export const ActiveSubscription = () =>
  SetMetadata(ACTIVE_SUBSCRIPTION_KEY, true);
