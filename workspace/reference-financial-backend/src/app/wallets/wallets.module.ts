import { User } from '@app/users/entity';
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import {
  Beneficiary,
  CryptoAccounts,
  FiatAccount,
  Transaction,
  Wallets,
  WalletSet,
} from './entities';
import { WalletsController } from './wallets.controller';
import {
  ConvertDefineService,
  ConvertService,
  SeerBitService,
  USDCService,
  WalletDefineService,
  WalletScheduler,
  WalletsService,
  WalletWebhookService,
} from './service';
import { Trades } from '@app/trades/entities';

@Module({
  imports: [
    TypeOrmModule.forFeature([
      FiatAccount,
      User,
      Wallets,
      Transaction,
      Beneficiary,
      WalletSet,
      CryptoAccounts,
      Trades,
    ]),
  ],
  controllers: [WalletsController],
  providers: [
    WalletsService,
    USDCService,
    SeerBitService,
    WalletScheduler,
    WalletWebhookService,
    WalletDefineService,
    ConvertService,
    ConvertDefineService,
  ],
  exports: [
    WalletsService,
    USDCService,
    SeerBitService,
    WalletScheduler,
    WalletWebhookService,
    WalletDefineService,
    ConvertService,
    ConvertDefineService,
  ],
})
export class WalletsModule {}
