import { User } from '@app/users/entity';
import { UsersModule } from '@app/users/users.module';
import { Transaction } from '@app/wallets/entities';
import { WalletsModule } from '@app/wallets/wallets.module';
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { ByBitGateway } from './bybit.gateway';
import {
  CopySettingEntity,
  FollowTraders,
  TradeActivityFeeds,
  Trades,
} from './entities';
import { PriceCache } from './price-caches';
import {
  ActivityService,
  BybitService,
  CopierService,
  CopierTradeService,
  CreateTradeService,
  ExecuteTradeService,
  TradeDefineService,
  TradeJobWorker,
  ProTradePerformance,
  TraderDefineService,
  TradesService,
  FollowingService,
  CopyTradeSettingsService,
} from './services';
import {
  TradesController,
  TraderController,
  CopierController,
  ActivitiesController,
  FollowController,
  CopyTradeSettingsController,
} from './controller';
import { PaymentService } from '@app/services';
import { SubscriptionModule } from '@app/subscription/subscription.module';

@Module({
  imports: [
    UsersModule,
    TypeOrmModule.forFeature([
      Trades,
      TradeActivityFeeds,
      FollowTraders,
      User,
      Transaction,
      CopySettingEntity,
    ]),
    WalletsModule,
    SubscriptionModule,
  ],
  controllers: [
    TradesController,
    TraderController,
    CopierController,
    ActivitiesController,
    FollowController,
    CopyTradeSettingsController,
  ],
  providers: [
    TradesService,
    PriceCache,
    ActivityService,
    TradeJobWorker,
    CreateTradeService,
    CopierTradeService,
    TradeDefineService,
    ExecuteTradeService,
    BybitService,
    ByBitGateway,
    TraderDefineService,
    ProTradePerformance,
    CopierService,
    PaymentService,
    FollowingService,
    CopyTradeSettingsService,
  ],
  exports: [TradesService, TradeJobWorker],
})
export class TradesModule {}
