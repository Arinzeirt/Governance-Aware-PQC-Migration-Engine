import { WaitList } from '@app/email-center/entities';
import { SecurityService } from '@app/helpers';
import { Trades } from '@app/trades/entities';
import { WalletsModule } from '@app/wallets/wallets.module';
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { JwtStrategy } from 'src/global/strategies/jwt.strategy';
import {
  ProtraderController,
  RoleController,
  UsersController,
} from './controller';
import { TwoFaController } from './controller/tfa.controller';
import { Privileges, Protrader, RoleModel, UserActivity } from './entity';
import { User } from './entity/user.entity';
import {
  AdminService,
  ProTraderService,
  RoleService,
  UsersService,
} from './service';
import { TwoFAService } from './service/twofa.service';
import { UserScheduleService } from './service/user-schdule.service';

@Module({
  imports: [
    TypeOrmModule.forFeature([
      User,
      RoleModel,
      Privileges,
      Protrader,
      WaitList,
      Trades,
      UserActivity,
    ]),
    WalletsModule,
  ],
  providers: [
    UsersService,
    RoleService,
    JwtStrategy,
    TwoFAService,
    SecurityService,
    ProTraderService,
    UserScheduleService,
    AdminService,
  ],
  controllers: [
    UsersController,
    RoleController,
    TwoFaController,
    ProtraderController,
  ],
  exports: [
    UsersService,
    JwtStrategy,
    RoleService,
    TwoFAService,
    ProTraderService,
    AdminService,
  ],
})
export class UsersModule {}
