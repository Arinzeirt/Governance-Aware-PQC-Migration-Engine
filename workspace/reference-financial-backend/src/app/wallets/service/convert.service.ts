import { AuthUser } from '@app/common';
import { User } from '@app/users/entity';
import { Role } from '@app/users/interface';
import {
  BadRequestException,
  ForbiddenException,
  forwardRef,
  Inject,
  Injectable,
} from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { InjectRepository } from '@nestjs/typeorm';
import { AxiosError } from 'axios';
import Big from 'big.js';
import { nanoid } from 'nanoid';
import { DataSource, Repository, TypeORMError } from 'typeorm';
import { v4 as uuidV4 } from 'uuid';
import { CryptoAccounts, Transaction, Wallets } from '../entities';
import {
  category,
  convert,
  convertResponse,
  transactionStatus,
  transactionType,
  walletSymbol,
} from '../input';
import { ConvertDefineService } from './convert-define.service';
import { WalletScheduler } from './scheduler.service';
import { USDCService } from './usdc.service';
import { HttpClientService } from '@app/services';
import { WalletDefineService } from './wallet-define.service';

@Injectable()
export class ConvertService extends WalletDefineService {
  constructor(
    @InjectRepository(Transaction)
    private readonly transRepo: Repository<Transaction>,
    @Inject(forwardRef(() => WalletScheduler))
    private readonly walletScheduler: WalletScheduler,
    @InjectRepository(CryptoAccounts)
    private readonly cryptoRepo: Repository<CryptoAccounts>,
    @InjectRepository(User)
    private readonly userRepo: Repository<User>,
    private readonly dataSource: DataSource,
    private readonly cdservice: ConvertDefineService,
    private readonly configService: ConfigService,
    @InjectRepository(Wallets)
    protected readonly walletRepo: Repository<Wallets>,
    protected readonly cryptoService: USDCService,
    protected readonly httpService: HttpClientService,
  ) {
    super(walletRepo, cryptoService, httpService);
  }

  async convertAsset(payload: convert, user: AuthUser) {
    const { from, to, amount } = payload;
    const reference = nanoid(20);
    const idempotency = uuidV4();

    try {
      if (from === to || to === from) {
        throw new ForbiddenException("Sorry you can't convert same currency");
      }
      const { converted } = await this.convert(payload);

      console.log(`Converting ${amount} ${from} to ${converted} ${to}`);

      // get user balance
      const bal = await this.userBalance(user);
      const { balance } = bal.wallets[from];

      if (!Big(balance).gte(Big(amount))) {
        throw new ForbiddenException('Insufficient balance');
      }

      let userWallet = await this.cryptoRepo.findOneBy({
        userId: user.id,
      });

      if (!userWallet) {
        userWallet = await this.cryptoService.createWalletForUser(user);
      }

      const admin = await this.userRepo.findOneBy({
        email: this.configService.getOrThrow<string>('ADMIN_EMAIL'),
      });
      if (!admin) return;

      let adminWallet = await this.cryptoRepo.findOneBy({
        userId: admin.id,
      });

      if (!adminWallet) {
        adminWallet = await this.cryptoService.createWalletForUser(admin);
      }

      if (from === walletSymbol.usdc) {
        return this.handleFromUsdcConversion(
          user,
          from,
          to,
          amount,
          converted,
          reference,
          idempotency,
          adminWallet,
        );
      }

      if (to === walletSymbol.usdc) {
        return this.handleToUsdcConversion(
          user,
          from,
          to,
          amount,
          converted,
          reference,
          idempotency,
          userWallet,
          admin,
        );
      }

      // convert for non usdc asset
      return this.handleNonUsdcConversion(
        user,
        from,
        to,
        amount,
        converted,
        reference,
      );
    } catch (error) {
      if (error instanceof TypeORMError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  async convert(dto: convert): Promise<convertResponse> {
    // For direct one-time conversions (not cached)
    const rates = await this.cdservice.getCachedRates();
    const result = this.cdservice.convertFromRates(
      { amount: dto.amount, from: dto.from, to: dto.to },
      rates,
    );

    return result;
  }

  private async handleNonUsdcConversion(
    user: AuthUser,
    from: walletSymbol,
    to: walletSymbol,
    amount: number,
    converted: number,
    reference: string,
  ) {
    return this.dataSource.manager.transaction(async (manager) => {
      const wallet = await this.lockAndFetchWallet(
        user.id,
        from,
        manager,
        false,
      );
      if (!wallet) throw new ForbiddenException('Insufficient balance');
      const walletPreviousBal = wallet.balance;
      const newBal = await this.applyWalletDelta(wallet, -amount, manager);

      // credit converted asset
      const receiverWallet = await this.lockAndFetchWallet(
        user.id,
        to,
        manager,
        false,
      );
      await this.applyWalletDelta(receiverWallet, converted, manager);

      return this.logTransactionHistory(
        {
          amount: amount,
          userId: user.id,
          type: transactionType.credit,
          category: category.convert,
          wallet: wallet,
          reference,
          previousBal: walletPreviousBal,
          currentBal: newBal,
          status: transactionStatus.success,
          description: `${from} to ${to}`,
        },
        manager,
      );
    });
  }

  private async handleToUsdcConversion(
    user: AuthUser,
    from: walletSymbol,
    to: walletSymbol,
    amount: number,
    converted: number,
    reference: string,
    idempotency: string,
    userWallet: CryptoAccounts,
    admin: User,
  ) {
    try {
      const debitAndKeepRecord = await this.dataSource.manager.transaction(
        async (manager) => {
          const senderWallet = await this.lockAndFetchWallet(
            user.id,
            from,
            manager,
            false,
          );

          if (!senderWallet) {
            throw new ForbiddenException('Insufficient balance');
          }

          const previousBal = senderWallet.balance;
          const senderNewBal = await this.applyWalletDelta(
            senderWallet,
            -amount,
            manager,
          );

          const transferDesc = `${from} to ${to}`;
          return await this.logTransactionHistory(
            {
              amount: amount,
              userId: user.id,
              type: transactionType.credit,
              category: category.convert,
              wallet: senderWallet,
              reference,
              idempotency,
              previousBal,
              currentBal: senderNewBal,
              status: transactionStatus.success,
              description: transferDesc,
            },
            manager,
          );
        },
      );

      const fundUserOnChain = await this.cryptoService.onChainTransfer(
        String(converted),
        userWallet.address,
        'LOW',
        {
          email: admin.email,
          role: Role.superAdmin,
          id: admin.id,
          roleLevel: admin.roleLevel,
          username: admin.username,
        },
      );

      debitAndKeepRecord.externalRef = fundUserOnChain?.id;
      debitAndKeepRecord.status = transactionStatus.initial;

      return this.transRepo.save(debitAndKeepRecord);
    } catch (error) {
      if (error instanceof TypeORMError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  private async handleFromUsdcConversion(
    user: AuthUser,
    from: walletSymbol,
    to: walletSymbol,
    amount: number,
    converted: number,
    reference: string,
    idempotency: string,
    adminWallet: CryptoAccounts,
  ) {
    try {
      // make on chain transaction
      const fundUserOnChain = await this.cryptoService.onChainTransfer(
        String(amount),
        adminWallet.address,
        'LOW',
        user,
      );

      // I want to keep record of the transaction
      return this.dataSource.manager.transaction(async (manager) => {
        const senderWallet = await this.lockAndFetchWallet(
          user.id,
          to,
          manager,
          false,
        );

        const delay = new Date(new Date().setTime(120_000)).getTime();
        this.walletScheduler.fundingUserAccount(
          {
            amount: String(converted),
            externalRef: fundUserOnChain?.id,
            currency: to,
            user,
          },
          delay,
        );
        const transferDesc = `${from} to ${to}`;
        return await this.logTransactionHistory(
          {
            amount,
            userId: user.id,
            type: transactionType.credit,
            category: category.convert,
            wallet: senderWallet,
            reference,
            idempotency,
            previousBal: senderWallet.balance,
            currentBal: senderWallet.balance,
            status: transactionStatus.initial,
            externalRef: fundUserOnChain?.id,
            description: transferDesc,
          },
          manager,
        );
      });
    } catch (error) {
      if (error instanceof AxiosError) {
        console.log(error.response?.data || error.message);
        throw new BadRequestException(error.response?.data || error.message);
      }
      if (error instanceof TypeORMError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }
}
