import { User } from '@app/users/entity';
import { Transaction } from '@app/wallets/entities';
import {
  transactionStatus,
  transactionType,
  walletSymbol,
} from '@app/wallets/input';
import { ConvertService, USDCService } from '@app/wallets/service';
import { CreateTransferTransactionForDeveloperResponseData } from '@circle-fin/developer-controlled-wallets';
import {
  BadRequestException,
  ForbiddenException,
  Injectable,
  InternalServerErrorException,
} from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { InjectRepository } from '@nestjs/typeorm';
import { AxiosError } from 'axios';
import Big from 'big.js';
import { nanoid } from 'nanoid';
import { Repository } from 'typeorm';
import {
  notification,
  paymentInput,
  paymentResponse,
} from './define.interface';
import { MailService, template } from '../mail';
import { OnEvent } from '@nestjs/event-emitter';

@Injectable()
export class PaymentService {
  constructor(
    @InjectRepository(Transaction)
    private readonly transRepo: Repository<Transaction>,

    @InjectRepository(User)
    private readonly userRepo: Repository<User>,

    private readonly configService: ConfigService,
    private readonly usdcService: USDCService,
    private readonly convertService: ConvertService,
    private readonly mailService: MailService,
  ) {}

  async internalDebitUser(
    payload: paymentInput,
    save: boolean = true,
  ): Promise<paymentResponse> {
    try {
      const email: string = this.configService.getOrThrow('ADMIN_EMAIL');
      const receiver = await this.userRepo.findOneBy({ email });
      if (!receiver) {
        throw new InternalServerErrorException('Something went wrong');
      }

      const admin_wallet = await this.usdcService.createWalletForUser(receiver);

      if (!admin_wallet) {
        throw new InternalServerErrorException('Something went wrong');
      }

      const { balances } = await this.usdcService.userWalletBalance(
        payload.user,
      );
      if (!balances) throw new ForbiddenException('Insufficient balance');
      const bal = Big(balances[0]?.amount || 0).gt(Big(payload.amount));
      if (!bal) throw new ForbiddenException('Insufficient balance');

      const response = await this.usdcService.onChainTransfer(
        String(payload.amount),
        admin_wallet.address,
        'LOW',
        payload.user,
      );

      const previous = Big(balances?.[0].amount ?? 0).toNumber();
      const current = Big(payload.amount).minus(Big(previous)).toNumber();

      const description = payload.symbol
        ? `$${payload.amount} was charge for trade ${payload.symbol}`
        : `$${payload.amount} was charge subscription `;

      if (save) {
        await this.transRepo.save(
          this.transRepo.create({
            amount: payload.amount,
            currentBal: current,
            description,
            previousBal: previous,
            reference: nanoid(20),
            status: transactionStatus.initial,
            type: transactionType.debit,
            category: payload.category,
            userId: payload.user.id,
            externalRef: response?.id,
          }),
        );
      }

      return { response, previous, current };
    } catch (error) {
      if (error instanceof AxiosError) {
        throw new BadRequestException(error.message);
      }
      if (error instanceof Error) {
        throw new BadRequestException(error.message);
      }

      throw error;
    }
  }

  async internalCreditUser(
    payload: paymentInput,
  ): Promise<CreateTransferTransactionForDeveloperResponseData | undefined> {
    try {
      const email: string = this.configService.getOrThrow('ADMIN_EMAIL');
      const admin = await this.userRepo.findOneBy({ email });
      if (!admin) return;

      const receiver = await this.usdcService.createWalletForUser(payload.user);

      if (!receiver) {
        //TODO send email to the user for missing wallet and save the payment for pending payment and reason it pending
        return;
      }

      const { balances } = await this.usdcService.userWalletBalance(admin);

      if (!balances) throw new ForbiddenException('Insufficient balance');
      const bal = Big(balances[0]?.amount || 0).gt(Big(payload.amount));

      if (!bal) {
        // TODO save it as a pending payment for admin to see and the reason the payment is pending
        return;
      }

      const response = await this.usdcService.onChainTransfer(
        String(payload.amount),
        receiver.address,
        'LOW',
        admin,
      );

      const previous = Big(balances?.[0].amount ?? 0).toNumber();
      const current = Big(payload.amount).minus(Big(previous)).toNumber();

      const description = `$${payload.amount} was paid to ${receiver.address}`;

      await this.transRepo.save(
        this.transRepo.create({
          amount: payload.amount,
          currentBal: current,
          description,
          previousBal: previous,
          reference: nanoid(20),
          status: transactionStatus.initial,
          type: transactionType.debit,
          category: payload.category,
          userId: admin.id,
          externalRef: response?.id,
          recipient: receiver.user,
        }),
      );

      return response;
    } catch (error) {
      if (error instanceof AxiosError) {
        throw new BadRequestException(error.message);
      }
      if (error instanceof Error) {
        throw new BadRequestException(error.message);
      }

      throw error;
    }
  }

  async convertCurrency(amount: number, isNaira: boolean = false) {
    const res = await this.convertService.convert({
      from: isNaira ? walletSymbol.naira : walletSymbol.usdc,
      to: isNaira ? walletSymbol.usdc : walletSymbol.naira,
      amount,
    });

    return res;
  }

  @OnEvent('payment.success', { async: true })
  private async sendNotification(payload: notification) {
    const formatted = new Intl.DateTimeFormat('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
      hour12: true,
      timeZone: 'Africa/Lagos',
    }).format(payload.dateAndTime);

    await this.mailService.sendMail(
      payload.email,
      template.notification,
      `${payload.sign} Payment Notification`,
      {
        amount: parseFloat(payload.amount).toLocaleString(),
        sign: payload.sign,
        accountNumber: payload.accountNumber,
        dateAndTime: formatted,
        balance: parseFloat(payload.balance).toLocaleString(),
      },
    );
  }
}
