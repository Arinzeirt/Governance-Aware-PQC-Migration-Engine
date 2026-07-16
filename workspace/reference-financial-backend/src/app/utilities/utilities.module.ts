import { UsersModule } from '@app/users/users.module';
import { WalletsModule } from '@app/wallets/wallets.module';
import { Module } from '@nestjs/common';
import {
  AirtimeService,
  DataService,
  DefineService,
  ElectricityService,
  ScheduleService,
} from './services';
import { UtilitiesController } from './utilities.controller';
import { TypeOrmModule } from '@nestjs/typeorm';
import { BillTnx } from './entities';
import { Transaction } from '@app/wallets/entities';

@Module({
  imports: [
    UsersModule,
    WalletsModule,
    TypeOrmModule.forFeature([BillTnx, Transaction]),
  ],
  controllers: [UtilitiesController],
  providers: [
    AirtimeService,
    DataService,
    ElectricityService,
    DefineService,
    ScheduleService,
  ],
})
export class UtilitiesModule {}
