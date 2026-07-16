import { AuthUser, Document, DocumentResult } from '@app/common';
import {
  buildFindManyQuery,
  FindManyWrapper,
  FindOneWrapper,
} from '@app/helpers';
import { User } from '@app/users/entity';
import {
  BadRequestException,
  ForbiddenException,
  Injectable,
  InternalServerErrorException,
} from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import * as bcrypt from 'bcrypt';
import Big from 'big.js';
import { nanoid } from 'nanoid';
import { DataSource, EntityManager, Repository, TypeORMError } from 'typeorm';

import { Beneficiary, Transaction, Wallets } from '../entities';
import {
  category,
  findManyBeneficiary,
  findManyTransaction,
  findOneBeneficiary,
  findOneTransaction,
  funding,
  internalTransfer,
  saveBeneficiary,
  transactionStatus,
  transactionType,
  walletSymbol,
} from '../input';
import { USDCService } from './usdc.service';
import { HttpClientService } from '@app/services';
import { WalletDefineService } from './wallet-define.service';

@Injectable()
export class WalletsService extends WalletDefineService {
  constructor(
    @InjectRepository(Transaction)
    private readonly transRepo: Repository<Transaction>,
    @InjectRepository(Beneficiary)
    private readonly beneficiary: Repository<Beneficiary>,
    @InjectRepository(Wallets)
    protected readonly walletRepo: Repository<Wallets>,
    private readonly dataSource: DataSource,
    protected readonly cryptoService: USDCService,
    protected httpService: HttpClientService,
  ) {
    super(walletRepo, cryptoService, httpService);
  }

  // TODO emit email error for admin notification

  async internalTransfer(dto: internalTransfer, user: AuthUser) {
    if (
      dto.recipientCurrency === walletSymbol.usdc ||
      dto.senderCurrency === walletSymbol.usdc
    ) {
      throw new BadRequestException(
        'Please user wallet transfer for usdc transaction',
      );
    }
    return this.dataSource.manager.transaction(async (manager) => {
      // check user password
      const findUser = await manager
        .createQueryBuilder(User, 'user')
        .addSelect('user.transactionPin')
        .where('user.email = :email', { email: user.email.toLowerCase() })
        .getOne();

      if (!findUser || !findUser.transactionPin) {
        throw new ForbiddenException('transaction pin not set');
      }

      const isMatch = await bcrypt.compare(
        dto.transactionPin,
        findUser.transactionPin,
      );

      if (!isMatch) {
        throw new ForbiddenException('Incorrect transaction pin');
      }

      // Idempotency: prevent double processing
      const existingTx = await this.checkIdempotency(dto.idempotency, manager);
      if (existingTx) {
        return {
          success: true,
          alreadyProcessed: true,
          transaction: existingTx,
        };
      }

      const reference = nanoid(20);

      // Fetch & lock sender wallet
      const senderWallet = await this.lockAndFetchWallet(
        user.id,
        dto.senderCurrency,
        manager,
        true,
      );
      if (!senderWallet) {
        throw new ForbiddenException(
          'Insufficient balance or account is under investigation',
        );
      }
      if (!Big(senderWallet.balance).gte(Big(dto.amount))) {
        throw new ForbiddenException('Insufficient balance');
      }

      // Fetch recipient user
      const recipient = await manager.findOne(User, {
        where: { username: dto.username },
      });
      if (!recipient) {
        throw new ForbiddenException('Recipient user not found');
      }

      // Debit sender
      const senderNewBal = await this.applyWalletDelta(
        senderWallet,
        -dto.amount,
        manager,
      );

      // Credit recipient
      const recipientWallet = await this.lockAndFetchWallet(
        recipient.id,
        dto.recipientCurrency,
        manager,
        false,
      );
      const recipientPrevBal = recipientWallet ? recipientWallet.balance : 0;

      const senderAmount = dto.amount;

      if (dto.senderCurrency !== dto.recipientCurrency) {
        // Convert amount based on cached rates
        const rates = await this.getCachedRates();
        const conversion = this.convertFromRates(
          {
            amount: dto.amount,
            from: dto.senderCurrency,
            to: dto.recipientCurrency,
          },
          rates,
        );
        dto.amount = conversion.converted;
      }

      // if (!recipientWallet) {
      //   recipientWallet = manager.create(Wallets, {
      //     currency: dto.recipientCurrency,
      //     user: { id: recipient.id },
      //     balance: dto.amount,
      //   });
      //   await manager.save(Wallets, recipientWallet);
      // } else {
      // }

      await this.applyWalletDelta(recipientWallet, dto.amount, manager);
      // save as beneficiary
      if (dto.beneficiary) {
        await this.saveBeneficiary(
          { recipient, userId: user.id, internal: true },
          manager,
        );
      }

      // Log histories
      const transferDesc = `Transfer ${senderAmount} ${dto.senderCurrency} from ${user.username ?? findUser.fullName} to ${recipient.username}`;
      await this.logTransactionHistory(
        {
          amount: senderAmount,
          userId: user.id,
          type: transactionType.debit,
          category: category.transfer,
          wallet: senderWallet,
          reference,
          idempotency: dto.idempotency,
          previousBal: senderWallet.balance,
          currentBal: senderNewBal,
          status: transactionStatus.success,
          description: transferDesc,
          recipient: recipient,
        },
        manager,
      );

      await this.logTransactionHistory(
        {
          amount: dto.amount,
          userId: recipient.id,
          type: transactionType.credit,
          category:
            dto.senderCurrency === walletSymbol.naira
              ? category.topup
              : category.deposit,
          wallet: recipientWallet,
          reference,
          previousBal: recipientPrevBal,
          currentBal: Big(recipientPrevBal).add(dto.amount).toNumber(),
          status: transactionStatus.success,
          description: `Received ${dto.amount} ${dto.recipientCurrency} from ${user.username ?? findUser.fullName}`,
        },
        manager,
      );

      return {
        success: true,
        transactionReference: reference,
        sender: { id: user.id, balance: senderNewBal },
        recipient: {
          id: recipient.id,
          balance: Big(recipientPrevBal).add(dto.amount).toNumber(),
        },
      };
    });
  }

  async adjustWallet(user: AuthUser, type: transactionType, data: funding) {
    return this.dataSource.manager.transaction(async (manager) => {
      // Idempotency check
      if (data.idempotency) {
        const idempotent = await this.checkIdempotency(
          data.idempotency,
          manager,
        );
        if (idempotent) {
          return {
            success: true,
            alreadyProcessed: true,
            transaction: idempotent,
          };
        }
      }

      if (type === transactionType.credit) {
        return this.fundWallet(user, data, manager);
      } else if (type === transactionType.debit) {
        return this.debitWallet(user, data, manager);
      } else {
        throw new BadRequestException('Invalid transaction type');
      }
    });
  }

  async findManyTransaction(
    query: findManyTransaction,
  ): Promise<DocumentResult<Transaction>> {
    try {
      const where = this.filterTransactions(query);
      const qb = this.transRepo.createQueryBuilder('transaction');
      buildFindManyQuery(
        qb,
        'transaction',
        where,
        query.search,
        [],
        query.include,
        query.sort,
      );

      return FindManyWrapper(qb, query.page, query.limit);
    } catch (error) {
      if (error instanceof TypeORMError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  async findOneTransaction(
    query: findOneTransaction,
  ): Promise<Document<Transaction>> {
    try {
      const { include, sort, ...filters } = query;

      return FindOneWrapper<Transaction>(this.transRepo, {
        include,
        sort,
        filters,
      });
    } catch (error) {
      if (error instanceof TypeORMError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  async findManyBeneficiary(
    query: findManyBeneficiary,
  ): Promise<DocumentResult<Beneficiary>> {
    try {
      const where = this.filterBeneficiary(query);
      const qb = this.beneficiary.createQueryBuilder('beneficiary');
      buildFindManyQuery(
        qb,
        'beneficiary',
        where,
        query.search,
        [
          'accountName',
          'bankName',
          'accountNumber',
          'recipient.fullName',
          'recipient.username',
          'recipient.email',
        ],
        query.include,
        query.sort,
        ['accountNumber'],
      );

      return FindManyWrapper(qb, query.page, query.limit);
    } catch (error) {
      if (error instanceof TypeORMError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  async findOneBeneficiary(
    query: findOneBeneficiary,
  ): Promise<Document<Beneficiary>> {
    try {
      const { include, sort, ...filters } = query;

      return FindOneWrapper<Beneficiary>(this.beneficiary, {
        include,
        sort,
        filters,
      });
    } catch (error) {
      if (error instanceof TypeORMError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  // save beneficiary
  private async saveBeneficiary(data: saveBeneficiary, manager: EntityManager) {
    try {
      const where: Record<string, any> = {};

      if (data.accountNumber) {
        where.accountNumber = data.accountNumber;
      } else if (data.recipient?.id) {
        where.recipient = { id: data.recipient.id };
      } else {
        throw new InternalServerErrorException('No search criteria provided');
      }

      const findIfExisted = await manager.findOne(Beneficiary, { where });

      if (findIfExisted) return findIfExisted;

      const saved = manager.create(Beneficiary, data);
      return await manager.save(Beneficiary, saved);
    } catch (error) {
      if (error instanceof TypeORMError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  private filterTransactions(data: findManyTransaction) {
    const where: Record<string, any> = {};
    if (data.userId) where['userId'] = data.userId;
    if (data.type) where['type'] = { $eq: data.type };
    if (data.status) where['status'] = { $eq: data.status };
    if (data.reference) where['reference'] = data.reference;
    if (data.amount) where['amount'] = data.amount;
    if (data.recipientId) {
      where['recipient'] = { 'recipient.id': data.recipientId };
    }
    return where;
  }

  private filterBeneficiary(data: findManyBeneficiary) {
    const where: Record<string, any> = {};
    if (data.accountName) where['accountName'] = data.accountName;
    if (data.accountNumber) where['accountNumber'] = data.accountNumber;
    if (data.bankName) where['bankName'] = data.bankName;
    if (data.userId) where['userId'] = data.userId;
    if (data.internal !== undefined) where['internal'] = { $eq: data.internal };
    if (data.fullName) {
      where['recipient'] = { 'recipient.fullName': data.fullName };
    }
    if (data.username) {
      where['recipient'] = { 'recipient.username': data.username };
    }
    return where;
  }
}
