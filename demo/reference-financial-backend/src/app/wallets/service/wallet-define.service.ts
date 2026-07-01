import { AuthUser } from '@app/common';
import { HttpClientService } from '@app/services';
import {
  BadRequestException,
  ForbiddenException,
  Injectable,
  Logger,
} from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import Big from 'big.js';
import { nanoid } from 'nanoid';
import { EntityManager, In, Repository, TypeORMError } from 'typeorm';
import { Transaction, Wallets } from '../entities';
import {
  category,
  funding,
  transactionStatus,
  transactionType,
  txnHistory,
  userBalResponse,
  walletStatus,
  walletSymbol,
} from '../input';
import { ConvertDefineService } from './convert-define.service';
import { USDCService } from './usdc.service';

@Injectable()
export class WalletDefineService extends ConvertDefineService {
  private readonly logger = new Logger(WalletDefineService.name);
  constructor(
    @InjectRepository(Wallets)
    protected readonly walletRepo: Repository<Wallets>,
    protected readonly cryptoService: USDCService,
    protected httpService: HttpClientService,
  ) {
    super(httpService);
  }

  async logTransactionHistory(data: txnHistory, manager: EntityManager) {
    // Optionally, pass logger in for audit trail
    try {
      const history = manager.create(Transaction, {
        ...data,
        wallet: { id: data?.wallet?.id },
      });
      return await manager.save(Transaction, history);
    } catch (error) {
      this.logger.error('Error logging transaction history', error.stack);
      if (error instanceof TypeORMError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  // Deposit funds into user's wallet.
  async fundWallet(user: AuthUser, data: funding, manager: EntityManager) {
    // Try to fetch wallet with lock; if not found, create it.
    let wallet = await this.lockAndFetchWallet(
      user.id,
      data.currency,
      manager,
      false,
    );
    const previousBal = wallet ? wallet.balance : 0;

    if (!wallet) {
      wallet = manager.create(Wallets, {
        user: { id: user.id },
        currency: data.currency,
        balance: data.amount,
      });
      await manager.save(Wallets, wallet);
    } else {
      await this.applyWalletDelta(wallet, data.amount, manager);
    }

    const reference = nanoid(20);

    // Log transaction history
    await this.logTransactionHistory(
      {
        amount: data.amount,
        userId: user.id,
        type: transactionType.debit,
        category:
          data.currency === walletSymbol.naira
            ? category.topup
            : category.deposit,
        wallet,
        idempotency: data.idempotency,
        reference,
        previousBal,
        currentBal: Big(previousBal).add(data.amount).toNumber(),
        status: transactionStatus.success,
        description: `Funded wallet with ${data.amount} ${data.currency}`,
      },
      manager,
    );

    return { success: true, reference, newBalance: wallet.balance };
  }

  // Debit (withdraw) funds from user's wallet.
  async debitWallet(user: AuthUser, data: funding, manager: EntityManager) {
    const wallet = await this.lockAndFetchWallet(
      user.id,
      data.currency,
      manager,
      true,
    );
    if (!wallet) {
      throw new ForbiddenException('No valid wallet to debit.');
    }
    if (!Big(wallet.balance).gte(Big(data.amount))) {
      throw new ForbiddenException('Insufficient balance for withdrawal.');
    }

    const previousBal = wallet.balance;
    await this.applyWalletDelta(wallet, -data.amount, manager);
    const reference = nanoid(20);

    await this.logTransactionHistory(
      {
        amount: data.amount,
        userId: user.id,
        type: transactionType.debit,
        category:
          data.currency === walletSymbol.naira
            ? category.topup
            : category.deposit,
        wallet,
        idempotency: data.idempotency,
        reference,
        previousBal,
        currentBal: Big(previousBal).sub(data.amount).toNumber(),
        status: transactionStatus.success,
        description: `Debited ${data.amount} ${data.currency} from wallet`,
      },
      manager,
    );

    return { success: true, reference, newBalance: wallet.balance };
  }

  //  Check if transaction with idempotency key exists
  async checkIdempotency(idempotency: string, manager: EntityManager) {
    if (!idempotency) return null;
    return manager.findOne(Transaction, { where: { idempotency } });
  }

  //  Fetch and lock wallet, optionally require active status
  async lockAndFetchWallet(
    userId: string,
    currency: walletSymbol,
    manager: EntityManager,
    enforceStatus: boolean,
  ) {
    const where = {
      user: { id: userId },
      currency,
      ...(enforceStatus && {
        status: In([walletStatus.active, walletStatus.warning]),
      }),
    };

    let userWallet = await manager.findOne(Wallets, {
      where,
      lock: { mode: 'pessimistic_write' },
    });

    if (!userWallet) {
      userWallet = await manager.save(
        manager.create(Wallets, {
          currency,
          user: { id: userId },
          balance: 0,
        }),
      );
    }

    return userWallet;
  }

  //  Apply delta (positive for credit, negative for debit), persist and return new balance
  async applyWalletDelta(
    wallet: Wallets,
    delta: number,
    manager: EntityManager,
  ) {
    const newBal = Big(wallet.balance).add(delta).toNumber();
    if (newBal < 0) throw new ForbiddenException('Balance cannot be negative');
    await manager.update(Wallets, { id: wallet.id }, { balance: newBal });
    wallet.balance = newBal;
    return newBal;
  }

  async userBalance(user: AuthUser): Promise<userBalResponse> {
    let totalUsd = 0;
    const walletSummaries = [];

    // Define all wallet types app supports
    const supportedCurrencies = ['NGN', 'USDC']; // 'STP',

    try {
      const userWallets = await this.walletRepo.find({
        where: { user: { id: user.id }, currency: walletSymbol.naira },
      });

      const { balances, wallet } =
        await this.cryptoService.userWalletBalance(user);
      if (balances?.length && wallet) {
        userWallets.push({
          balance: Big(balances[0].amount).toNumber(),
          currency: walletSymbol.usdc,
          user: wallet.user,
          id: wallet.id,
          transactions: [],
          status: walletStatus.active,
          createdAt: wallet.createDate,
          updatedAt: wallet.updateDate,
        });
      }

      // ✅ Fetch cached rates once
      const rates = await this.getCachedRates();

      // Convert each wallet balance to USD
      for (const wallet of userWallets) {
        const { balance, currency } = wallet;
        const usdValue = this.convertFromRates(
          { amount: balance, from: currency, to: walletSymbol.dollar },
          rates,
        );

        walletSummaries.push({
          currency,
          balance,
          usdValue: Number(usdValue.converted.toFixed(2)),
        });

        totalUsd += usdValue.converted;
      }

      // ✅ Add missing wallets with zero balances
      for (const currency of supportedCurrencies) {
        const exists = walletSummaries.find((w) => w.currency === currency);
        if (!exists) {
          walletSummaries.push({
            currency,
            balance: 0,
            usdValue: 0,
          });
        }
      }

      // Sort the wallets in the defined order
      walletSummaries.sort(
        (a, b) =>
          supportedCurrencies.indexOf(a.currency) -
          supportedCurrencies.indexOf(b.currency),
      );

      // Transform array to object keyed by currency
      const walletsObj = walletSummaries.reduce(
        (acc, w) => {
          acc[w.currency] = { balance: w.balance, usdValue: w.usdValue };
          return acc;
        },
        {} as Record<string, { balance: number; usdValue: number }>,
      );

      return {
        totalUsd: Number(totalUsd.toFixed(2)),
        wallets: walletsObj,
      };
    } catch (error) {
      // console.log(error);
      if (error instanceof BadRequestException) {
        throw new BadRequestException('Error fetching wallet balances');
      }
      throw error;
    }
  }
}
