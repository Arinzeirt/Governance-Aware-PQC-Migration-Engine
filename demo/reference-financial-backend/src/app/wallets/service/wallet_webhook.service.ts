import { AuthUser } from '@app/common';
import { IUser, Role } from '@app/users/interface';
import { TransactionBound, transactionData } from '@app/webhooks/index';
import {
  BadRequestException,
  ForbiddenException,
  Injectable,
} from '@nestjs/common';
import { EventEmitter2, OnEvent } from '@nestjs/event-emitter';
import { InjectRepository } from '@nestjs/typeorm';
import Big from 'big.js';
import { nanoid } from 'nanoid';
import { Repository, TypeORMError } from 'typeorm';
import { CryptoAccounts, Transaction } from '../entities';
import { category, transactionStatus, transactionType } from '../input';
import { USDCService } from './usdc.service';
import { User } from '@app/users/entity';

@Injectable()
export class WalletWebhookService {
  constructor(
    @InjectRepository(Transaction)
    private readonly transRepo: Repository<Transaction>,
    @InjectRepository(CryptoAccounts)
    private readonly cryptoRepo: Repository<CryptoAccounts>,
    @InjectRepository(User)
    private readonly userRepo: Repository<User>,
    private eventEmitter: EventEmitter2,
    private readonly usdcService: USDCService,
  ) {}

  @OnEvent('tnx.outbound')
  async HandleTransactionOutBound(payload: TransactionBound) {
    console.log('Outbound Transaction Payload:', payload.notification.state);
    const transaction = await this.transRepo.findOne({
      where: {
        externalRef: payload.notification.id,
      },
      relations: ['user'],
    });

    // console.log('Outbound Transaction Payload:', { transaction, payload });
    // const isTrade = await this.tradeRepo.findOneBy({
    //   fundId: payload.notification.id,
    // });

    // Already processed
    if (transaction) {
      const status = payload.notification.state;
      if (transaction.category === category.trade) {
        if (status === transactionStatus['confirmed']) {
          const data = {
            fundId: payload.notification.id,
          };
          await this.eventEmitter.emitAsync('execute.trade', data);
        }
      }

      if (transaction.category === category.subscription) {
        if (status === transactionStatus['confirmed']) {
          const data = { paymentId: payload.notification.id };
          await this.eventEmitter.emitAsync('execute.subscription', data);
        }
      }

      if (
        [category.airtime, category.data, category.electricity].includes(
          transaction.category,
        )
      ) {
        if (status === transactionStatus['confirmed']) {
          const data = { paymentId: payload.notification.id };
          await this.eventEmitter.emitAsync('execute.utility', data);
        }
      }

      if (status === transactionStatus['confirmed']) {
        // send notification to user
        this.eventEmitter.emitAsync('payment.success', {
          email: transaction.user.email,
          amount: transaction.amount,
          sign: 'USDC',
          accountNumber: payload.notification.sourceAddress,
          dateAndTime: transaction.createdAt,
          balance: transaction.currentBal,
        });
      }

      await this.transRepo.update(
        { externalRef: payload.notification.id },
        { status },
      );
      return;
    }

    // Keep the record of new transaction
    const { sender, receiver } = await this.handleSenderAndReceiver(payload);

    const amt = Big(payload.notification.amounts[0]).toNumber();
    if (sender) {
      const user: AuthUser = {
        email: sender.user.email,
        username: sender.user.username,
        role: sender.user.role ?? Role.follower,
        roleLevel: sender.user.roleLevel,
        id: sender.user.id,
      };

      const { balances } = await this.usdcService.userWalletBalance(user);
      if (!balances || !balances.length) {
        throw new ForbiddenException('User balance not found');
      }

      const currentBal = Big(balances[0].amount);
      const previousBal = currentBal.add(Big(amt)).toNumber();
      const transferDesc = `${receiver ? 'Transfer' : 'Withdraw'} ${amt} USDC to ${payload.notification.destinationAddress}`;

      const rec = receiver?.user;
      await this.TransactionLog(
        amt,
        currentBal.toNumber(),
        transferDesc,
        previousBal,
        payload.notification.state,
        sender.user.id,
        payload.notification.id,
        rec,
      );
    }
    return;
  }

  @OnEvent('tnx.inbound')
  async HandleTransactionInBound(payload: TransactionBound) {
    // console.log('Inbound Transaction Payload:', payload.notification.state);
    const findWallet = await this.cryptoRepo.findOne({
      where: {
        address: payload.notification.destinationAddress,
      },
      relations: ['user'],
    });

    if (!findWallet) return;

    const findTransaction = await this.transRepo.findOneBy({
      externalRef: payload.notification.id,
    });

    if (!findWallet.user.quickStart.fundWallet) {
      findWallet.user.quickStart.fundWallet = true;
      findWallet.user.quickStart.firstTrade = false;
      await this.userRepo.save(findWallet.user);
    }

    if (!findTransaction) {
      return await this.handleInTransaction(payload, findWallet);
    }

    const status = payload.notification.state;
    if (status === transactionStatus['complete']) {
      this.eventEmitter.emitAsync('payment.success', {
        email: findWallet.user.email,
        amount: payload.notification.amounts[0],
        sign: 'USDC',
        accountNumber: findWallet.address,
        dateAndTime: new Date(),
        balance: findTransaction.currentBal,
      });
    }

    return await this.transRepo.update(
      { externalRef: payload.notification.id },
      {
        status: payload.notification.state,
        txHash: payload.notification.txHash,
        networkFee: payload.notification.networkFee,
        userOpHash: payload.notification.userOpHash,
        errorDetails: JSON.stringify(payload.notification.errorDetails),
      },
    );
  }

  @OnEvent('web.text')
  HandleWebhookTest(payload: any) {
    console.log(payload);
  }

  @OnEvent('tnx.in')
  HandleSeerBitTransaction(payload: transactionData) {
    try {
      console.log('Transaction', payload);
    } catch (error) {
      if (error instanceof TypeORMError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  @OnEvent('tnx.out')
  HandleSeerBitTransactionWallet(payload: transactionData) {
    try {
      console.log('Transaction Wallet', payload);
    } catch (error) {
      if (error instanceof TypeORMError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  private async handleSenderAndReceiver(payload: TransactionBound) {
    const [sender, receiver] = await Promise.allSettled([
      this.cryptoRepo.findOne({
        where: {
          address: payload.notification.sourceAddress,
        },
        relations: ['user'],
      }),

      this.cryptoRepo.findOne({
        where: {
          address: payload.notification.destinationAddress,
        },
        relations: ['user'],
      }),
    ]);

    if (sender.status === 'fulfilled' && receiver.status === 'fulfilled') {
      return { sender: sender.value, receiver: receiver.value };
    }

    if (sender.status === 'fulfilled' && receiver.status === 'rejected') {
      return { sender: sender.value, receiver: null };
    }

    if (sender.status === 'rejected' && receiver.status === 'fulfilled') {
      return { sender: null, receiver: receiver.value };
    }

    return { sender: null, receiver: null };
  }

  private async TransactionLog(
    amt: number,
    currentBal: number,
    desc: string,
    previousBal: number,
    status: transactionStatus,
    userId: string,
    externalRef: string,
    receiver?: IUser,
  ) {
    return await this.transRepo.save(
      this.transRepo.create({
        amount: amt,
        currentBal,
        description: desc,
        previousBal,
        reference: nanoid(20),
        status,
        type: transactionType.debit,
        category: receiver ? category.transfer : category.withdraw,
        userId,
        externalRef,
        recipient: receiver,
      }),
    );
  }

  private async handleInTransaction(
    payload: TransactionBound,
    findWallet: { user: IUser },
  ) {
    const { user } = findWallet;
    const amount = Big(payload.notification.amounts[0]).toNumber();
    const { balances: bal } = await this.usdcService.userWalletBalance({
      id: user.id,
      username: user.username,
      email: user.email,
      role: user.role ?? Role.follower,
      roleLevel: user.roleLevel,
    });
    const previous = Big(bal?.[0].amount ?? 0).toNumber();
    const current = Big(amount).add(Big(previous)).toNumber();
    return this.transRepo.save(
      this.transRepo.create({
        amount,
        currentBal: current,
        description: `Received ${amount} USDC from ${payload.notification.sourceAddress}`,
        previousBal: previous,
        reference: nanoid(20),
        status: payload.notification.state,
        type: transactionType.credit,
        category: category.deposit,
        userId: findWallet.user.id,
        txHash: payload.notification.txHash,
        networkFee: payload.notification.networkFee,
        userOpHash: payload.notification.userOpHash,
        errorDetails: JSON.stringify(payload.notification.errorDetails),
        externalRef: payload.notification.id,
      }),
    );
  }
}
