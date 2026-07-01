import { TradesModule } from '@app/trades/trades.module';
import { User } from '@app/users/entity';
import { Transaction } from '@app/wallets/entities';
import { WalletsModule } from '@app/wallets/wallets.module';
import { HttpModule } from '@nestjs/axios';
import { forwardRef, Global, Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { DiscoveryModule } from '@nestjs/core';
import { TypeOrmModule } from '@nestjs/typeorm';
import { EmailCenterModule } from 'src/app/email-center/email-center.module';
import {
  FileProcessorService,
  HtmlChunkerService,
  HttpClientService,
  MailService,
  PaymentService,
  SanitizeService,
  UploadService,
  WebSocketService,
} from './services';

@Global()
@Module({
  imports: [
    TypeOrmModule.forFeature([Transaction, User]),
    ConfigModule,
    DiscoveryModule,
    forwardRef(() => EmailCenterModule),
    forwardRef(() => TradesModule),
    WalletsModule,
    HttpModule.registerAsync({
      useFactory: () => ({
        timeout: 5000,
        maxRedirects: 5,
      }),
    }),
  ],
  providers: [
    MailService,
    UploadService,
    SanitizeService,
    FileProcessorService,
    HtmlChunkerService,
    HttpClientService,
    WebSocketService,
    PaymentService,
  ],
  exports: [
    MailService,
    UploadService,
    SanitizeService,
    FileProcessorService,
    HtmlChunkerService,
    HttpClientService,
    WebSocketService,
    PaymentService,
  ],
})
export class GlobalModule {}
