import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { SubPlans, Subscription, SubscriptionHistory } from './entities';
import {
  HistoryService,
  PlanService,
  SubscriptionJobService,
  SubscriptionService,
} from './service';
import { SubscriptionController } from './subscription.controller';

@Module({
  imports: [
    TypeOrmModule.forFeature([Subscription, SubscriptionHistory, SubPlans]),
  ],
  controllers: [SubscriptionController],
  providers: [
    SubscriptionService,
    SubscriptionJobService,
    PlanService,
    HistoryService,
  ],
  exports: [
    SubscriptionService,
    SubscriptionJobService,
    PlanService,
    HistoryService,
  ],
})
export class SubscriptionModule {}
