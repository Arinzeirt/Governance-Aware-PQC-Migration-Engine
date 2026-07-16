import { AuthUser } from '@app/common';
import { HttpClientService, PaymentService } from '@app/services';
import { UsersService } from '@app/users/service';
import { Transaction } from '@app/wallets/entities';
import {
  category,
  transactionStatus,
  transactionType,
  walletSymbol,
} from '@app/wallets/input';
import { WalletDefineService } from '@app/wallets/service';
import {
  BadGatewayException,
  BadRequestException,
  ForbiddenException,
  forwardRef,
  Inject,
  Injectable,
  InternalServerErrorException,
  NotFoundException,
} from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { InjectRepository } from '@nestjs/typeorm';
import { AxiosError } from 'axios';
import * as bcrypt from 'bcrypt';
import { addHours } from 'date-fns';
import { nanoid } from 'nanoid';
import { DataSource, EntityManager, Repository, TypeORMError } from 'typeorm';
import { BillTnx } from '../entities';
import { createBill, processPayment, requery, utilityResponse } from '../input';
import { ScheduleService } from './schedule.service';

@Injectable()
export class DefineService {
  constructor(
    private readonly httpService: HttpClientService,
    private readonly configService: ConfigService,
    private readonly userService: UsersService,
    private readonly dataSource: DataSource,
    private readonly wdService: WalletDefineService,

    @InjectRepository(Transaction)
    private readonly transRepository: Repository<Transaction>,
    @InjectRepository(BillTnx)
    private readonly billsRepository: Repository<BillTnx>,
    @Inject(forwardRef(() => ScheduleService))
    private readonly scheduleService: ScheduleService,
    private readonly paymentService: PaymentService,
  ) {}

  async checkedPin(pin: string, user: AuthUser): Promise<boolean> {
    try {
      const findUser = await this.userService.login(user.email);
      if (!findUser) {
        throw new ForbiddenException('user not found');
      }

      if (!findUser.hasTransactionPin || !findUser.transactionPin) {
        throw new ForbiddenException('Please set your transaction pin');
      }

      return bcrypt.compare(pin, findUser.transactionPin);
    } catch (error) {
      if (error instanceof TypeORMError) {
        throw new InternalServerErrorException();
      }
      throw error;
    }
  }

  async handlePayment(
    payload: processPayment,
    user: AuthUser,
    bill: createBill,
  ) {
    try {
      // Convert the amount to from Naira to USDC
      const { converted: amountInUSDC } =
        await this.paymentService.convertCurrency(payload.amount, true);

      // Debit user wallet for the payment
      const payment = await this.paymentService.internalDebitUser(
        {
          amount: amountInUSDC,
          category: payload.service,
          user: user,
        },
        false,
      );

      // Create transaction history
      return this.dataSource.manager.transaction(async (manager) => {
        const existingTx = await this.wdService.checkIdempotency(
          payload.idempotency,
          manager,
        );

        if (existingTx) {
          return {
            success: true,
            alreadyProcessed: true,
            transaction: existingTx,
          };
        }

        const reference = nanoid(20);
        // TODO remove the comment if not useing USDC for payments
        // const wallet = await this.wdService.lockAndFetchWallet(
        //   user.id,
        //   walletSymbol.naira,
        //   manager,
        //   true,
        // );

        // if (!wallet) {
        //   throw new ForbiddenException(
        //     'Insufficient balance or account is under investigation',
        //   );
        // }

        // if (!Big(wallet.balance).gte(Big(payload.amount))) {
        //   throw new ForbiddenException('Insufficient balance');
        // }

        // const newBal = await this.wdService.applyWalletDelta(
        //   wallet,
        //   -payload.amount,
        //   manager,
        // );

        const bills = await manager.save(
          BillTnx,
          manager.create(BillTnx, bill),
        );
        const transferDesc = `Purchase ${payload.service} of N${payload.amount}`;
        const transResponse = await this.wdService.logTransactionHistory(
          {
            amount: payload.amount,
            userId: user.id,
            type: transactionType.debit,
            category: payload.service,
            // wallet: wallet,
            idempotency: payload.idempotency,
            reference,
            previousBal: payment.previous,
            currentBal: payment.current,
            status: transactionStatus.initial,
            description: transferDesc,
            bills,
            externalRef: payment.response?.id,
          },
          manager,
        );

        return {
          success: true,
          alreadyProcessed: false,
          transaction: transResponse,
        };
      });
    } catch (error: unknown) {
      if (error instanceof TypeORMError) {
        throw new InternalServerErrorException();
      }
      throw error;
    }
  }

  async requeryTransaction(payload: requery) {
    try {
      const windowStart = payload.createdAt;
      const windowEnd = addHours(windowStart, 24);
      if (new Date() > windowEnd) return;

      const transaction = await this.transRepository.findOne({
        where: {
          externalRef: payload.request_id,
          status: transactionStatus.pending,
        },
        relations: ['bills'],
      });

      if (!transaction) {
        throw new NotFoundException('Transaction not found');
      }

      const response = await this.httpService.post<utilityResponse>({
        uri: `${this.configService.getOrThrow('VTPASS_URI')}/requery`,
        body: { request_id: payload.request_id },
        headers: {
          'api-key': this.configService.getOrThrow('VTPASS_API_KEY'),
          'secret-key': this.configService.getOrThrow('VTPASS_SECRET_KEY'),
        },
      });
      const status = response.content.transactions.status;

      switch (status) {
        case 'initiated':
          transaction.status = transactionStatus.initial;
          this.scheduleService.scheduleRequery(payload, 50000);
          break;
        case 'pending':
          this.scheduleService.scheduleRequery(payload, 50000);
          transaction.status = transactionStatus.pending;
          break;
        case 'delivered':
          if (transaction.category === category.electricity) {
            if (transaction.bills) {
              const bill = await this.billsRepository.findOne({
                where: { id: transaction.bills['id'] },
              });

              if (bill) {
                bill.meterToken = response.mainToken;
                bill.bundleSize = String(response.mainTokenTax);

                await this.billsRepository.save(bill);
              }
            }
          }
          transaction.status = transactionStatus.success;
          break;
        default:
          transaction.status = transactionStatus.fail;
          break;
      }

      await this.transRepository.save(transaction);
      return response;
    } catch (error) {
      if (error instanceof AxiosError) {
        throw new BadGatewayException(error.message);
      }
      throw error;
    }
  }

  async handleUtilityPayment(
    payload: Record<string, string | number>,
  ): Promise<utilityResponse> {
    try {
      const response = await this.httpService.post<utilityResponse>({
        uri: `${this.configService.getOrThrow('VTPASS_URI')}/pay`,
        body: payload,
        headers: {
          'api-key': this.configService.getOrThrow('VTPASS_API_KEY'),
          'secret-key': this.configService.getOrThrow('VTPASS_SECRET_KEY'),
        },
      });

      return response;
    } catch (error) {
      if (error instanceof AxiosError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  async handleUtilityPurchase(
    result: utilityResponse,
    transaction: Transaction,
    user: AuthUser,
  ) {
    try {
      switch (result.code) {
        case '000':
          console.log(
            'Transaction processed; requery to confirm final status (initiated/pending/delivered).',
          );

          this.scheduleService.scheduleRequery(
            {
              request_id: result.requestId,
              createdAt: transaction.createdAt,
            },
            10000,
          );
          break;
        case '099':
          console.log('Transaction is processing; scheduling requery.');
          this.scheduleService.scheduleRequery(
            {
              request_id: result.requestId,
              createdAt: transaction.createdAt,
            },
            10000,
          );
          break;
        case '001':
          console.log('Transaction query response received.');
          this.scheduleService.scheduleRequery(
            {
              request_id: result.requestId,
              createdAt: transaction.createdAt,
            },
            10000,
          );
          break;
        case '044':
          console.log('Transaction resolved; contact support for details.');
          this.scheduleService.scheduleRequery(
            {
              request_id: result.requestId,
              createdAt: transaction.createdAt,
            },
            10000,
          );
          break;
        case '091':
          console.log('Transaction not processed; no charge applied.');
          // await this.handleFailedTransaction(user.id, transaction);
          this.scheduleService.scheduleRequery(
            {
              request_id: result.requestId,
              createdAt: transaction.createdAt,
            },
            10000,
          );
          break;
        case '016':
          console.log('Transaction failed.');
          // await this.handleFailedTransaction(user.id, transaction);
          this.scheduleService.scheduleRequery(
            {
              request_id: result.requestId,
              createdAt: transaction.createdAt,
            },
            10000,
          );
          break;
        case '089':
          console.log(
            'Previous request is still processing; scheduling requery.',
          );
          this.scheduleService.scheduleRequery(
            {
              request_id: result.requestId,
              createdAt: transaction.createdAt,
            },
            10000,
          );
          break;
        case '010':
        case '011':
        case '012':
        case '013':
        case '014':
        case '015':
        case '017':
        case '018':
        case '019':
        case '021':
        case '022':
        case '023':
        case '024':
        case '025':
        case '026':
        case '027':
        case '028':
        case '030':
        case '031':
        case '032':
        case '034':
        case '035':
        case '040':
        case '083':
        case '085':
        case '087':
          console.log(
            `Provider returned error code ${result.code}: ${result.response_description ?? 'see provider documentation for details.'}`,
          );
          // await this.handleFailedTransaction(user.id, transaction);
          this.scheduleService.scheduleRequery(
            {
              request_id: result.requestId,
              createdAt: transaction.createdAt,
            },
            10000,
          );
          break;
        default:
          console.log(`Unhandled response code: ${result.code}`);
          this.scheduleService.scheduleRequery(
            {
              request_id: result.requestId,
              createdAt: transaction.createdAt,
            },
            10000,
          );
          break;
      }
      return result;
    } catch (error) {
      if (error instanceof AxiosError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  async handleFailedTransaction(
    userId: string,
    transaction: Transaction,
  ): Promise<void> {
    await this.dataSource.manager.transaction(
      async (manager: EntityManager): Promise<void> => {
        const wallet = await this.wdService.lockAndFetchWallet(
          userId,
          walletSymbol.naira,
          manager,
          false,
        );

        const newBalance = await this.wdService.applyWalletDelta(
          wallet,
          transaction.amount,
          manager,
        );

        transaction.status = transactionStatus.fail;
        transaction.currentBal = newBalance;
        await manager.save(Transaction, transaction);
        return;
      },
    );
  }
}
