import { AuthUser } from '@app/common';
import { User } from '@app/users/entity';
import {
  CreateTransferTransactionForDeveloperResponseData,
  FeeLevel,
  generateEntitySecret,
  generateEntitySecretCiphertext,
  initiateDeveloperControlledWalletsClient,
  registerEntitySecretCiphertext,
} from '@circle-fin/developer-controlled-wallets';
import {
  BadRequestException,
  ForbiddenException,
  Injectable,
  InternalServerErrorException,
  NotFoundException,
} from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { InjectRepository } from '@nestjs/typeorm';
import * as bcrypt from 'bcrypt';
import Big from 'big.js';
import { writeFileSync } from 'fs';
import { nanoid } from 'nanoid';
import { join } from 'path';
import { Repository } from 'typeorm';
import { v4 as uuidV4 } from 'uuid';
import { CryptoAccounts, WalletSet } from '../entities';
import { cryptoTransfer } from '../input';
import { HttpClientService } from '@app/services';
import * as forge from 'node-forge';

@Injectable()
export class USDCService {
  constructor(
    @InjectRepository(WalletSet)
    private readonly walletSetRepo: Repository<WalletSet>,
    @InjectRepository(CryptoAccounts)
    private readonly cryptoRepo: Repository<CryptoAccounts>,
    @InjectRepository(User) private readonly userRepo: Repository<User>,
    private readonly configService: ConfigService,
    private readonly httpService: HttpClientService,
  ) {}

  async createWalletForUser(data: string | AuthUser): Promise<CryptoAccounts> {
    try {
      const user: AuthUser =
        typeof data === 'string' ? (JSON.parse(data) as AuthUser) : data;

      // check if user have crypto wallet before
      const hasCryptoWallet = await this.cryptoRepo.findOneBy({
        userId: user.id,
      });

      if (hasCryptoWallet) return hasCryptoWallet;

      // Find or create wallet set
      const findWalletSet = await this.createWalletSet();
      // console.log({ findWalletSet });

      if (!findWalletSet) throw new NotFoundException('WalletSet not found');

      const client = this.initiateDeveloper();
      const blockchain = this.configService.getOrThrow('BLOCKCHAIN');
      const response = await client.createWallets({
        blockchains: [blockchain],
        count: 1,
        accountType: 'SCA',
        walletSetId: findWalletSet.walletId,
      });

      // console.log({ response: response.data?.wallets });

      let walletResponse: CryptoAccounts | null = null;
      if (response.data?.wallets) {
        const { wallets } = response.data;
        walletResponse = await this.cryptoRepo.save(
          this.cryptoRepo.create({
            circleId: wallets[0].id,
            state: wallets[0].state,
            walletSetId: findWalletSet.id,
            custodyType: wallets[0].custodyType,
            address: wallets[0].address,
            blockchain: wallets[0].blockchain,
            initialPublicKey: wallets[0].initialPublicKey,
            name: wallets[0].name,
            refId: wallets[0].refId,
            circleUserId: wallets[0].userId,
            userId: user.id,
            updateDate: wallets[0].updateDate,
            createDate: wallets[0].createDate,
          }),
        );
      }

      if (!walletResponse) {
        throw new Error('Wallet response could not be generated.');
      }

      return walletResponse;
    } catch (error) {
      if (error instanceof Error) {
        console.log(error);
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  async createWalletSet(): Promise<WalletSet> {
    try {
      const name = `STP-${nanoid(10)}`;

      //  1. Look for the currently active wallet-set
      const activeWallet = await this.walletSetRepo.findOneBy({
        isActive: true,
      });

      //  2. Decide what to do with it
      if (activeWallet) {
        const walletCount = await this.cryptoRepo.countBy({
          name: activeWallet.name,
        });

        if (walletCount < 10_000) {
          return activeWallet;
        }

        // rule-2 : hit the limit → force retire this set
        activeWallet.isActive = false;
        await this.walletSetRepo.save(activeWallet);
      }

      /* ---------------------------------------------------------
       * 3. We reach here when
       *    – there was no active wallet-set at all (rule-1), or
       *    – the previous one was just retired (rule-2)
       *    → create a brand-new wallet-set
       * --------------------------------------------------------- */
      const client = this.initiateDeveloper();
      const response = await client.createWalletSet({
        name,
        idempotencyKey: uuidV4(),
      });

      if (!response.data?.walletSet) {
        throw new InternalServerErrorException('Wallet set not created');
      }

      const { walletSet } = response.data;
      return this.walletSetRepo.save(
        this.walletSetRepo.create({
          walletId: walletSet.id,
          name,
          custodyType: 'DEVELOPER',
          createDate: walletSet.createDate,
          updateDate: walletSet.updateDate,
          isActive: true,
        }),
      );
    } catch (error) {
      console.log(error);
      if (error instanceof Error) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  async userWalletBalance(user: AuthUser) {
    try {
      const userWallet = await this.cryptoRepo.findOneBy({
        userId: user.id,
      });

      if (!userWallet) {
        return { balances: [] };
      }
      const client = this.initiateDeveloper();
      const response = await client.getWalletTokenBalance({
        id: userWallet.circleId, //id of the generated wallet
      });

      // console.log(response.data);

      return { balances: response.data?.tokenBalances, wallet: userWallet };
    } catch (error) {
      if (error instanceof Error) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  async createCryptoTransaction(dto: cryptoTransfer, user: AuthUser) {
    try {
      const { amount, walletAddress, feeLevel, transactionPin } = dto;

      // check user password
      const findUser = await this.userRepo
        .createQueryBuilder('user')
        .addSelect('user.transactionPin')
        .where('user.email = :email', { email: user.email.toLowerCase() })
        .getOne();

      if (!findUser || !findUser.transactionPin) {
        throw new ForbiddenException('transaction pin not set');
      }

      const isMatch = await bcrypt.compare(
        transactionPin,
        findUser.transactionPin,
      );

      if (!isMatch) {
        throw new ForbiddenException('Incorrect transaction pin');
      }
      return this.onChainTransfer(amount, walletAddress, feeLevel, user);
    } catch (error) {
      if (error instanceof Error) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  async onChainTransfer(
    amount: string,
    walletAddress: string,
    feeLevel: FeeLevel,
    user: AuthUser,
  ): Promise<CreateTransferTransactionForDeveloperResponseData | undefined> {
    try {
      const { balances, wallet } = await this.userWalletBalance(user);
      if (!balances || !balances.length || !wallet) {
        throw new ForbiddenException('User balance not found');
      }

      const previousBal = Big(balances[0].amount);
      if (previousBal.lt(Big(amount))) {
        throw new ForbiddenException('Insufficient Balance');
      }

      const currentBal = previousBal.minus(Big(amount));
      if (currentBal.lt(Big(0))) {
        throw new ForbiddenException('Insufficient Balance');
      }

      const client = this.initiateDeveloper();
      const response = await client.createTransaction({
        walletId: wallet.circleId,
        tokenId: balances[0].token.id,
        destinationAddress: walletAddress,
        amount: [amount],
        fee: { type: 'level', config: { feeLevel } },
      });

      return response.data;
    } catch (error) {
      if (error instanceof Error) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  private initiateDeveloper() {
    return initiateDeveloperControlledWalletsClient({
      apiKey: this.configService.getOrThrow('CIRCLE_API_KEY'),
      entitySecret: this.configService.getOrThrow('CIRCLE_ENTITY_SECRET'),
    });
  }

  private async generateEnSecretCiphertext(entitySecret: string) {
    // This will generate the Entity Secret Ciphertext.
    return await generateEntitySecretCiphertext({
      apiKey: this.configService.getOrThrow('CIRCLE_API_KEY'),
      entitySecret,
    });
  }

  private generateSecret() {
    // This will print out a new entity secret and sample code to register the entity secret
    const entitySecret = generateEntitySecret();
    console.log(entitySecret);
  }

  private async getPublicKeyForEntity() {
    try {
      const response = await this.httpService.get({
        uri: 'https://api.circle.com/v1/w3s/config/entity/publicKey',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${this.configService.getOrThrow('CIRCLE_API_KEY')}`,
        },
      });
      return response.data;
    } catch (error) {
      if (error instanceof Error) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  private async getEnscreteManually() {
    try {
      const entitySecret = forge.util.hexToBytes(
        this.configService.getOrThrow('CIRCLE_ENTITY_SECRET'),
      );
      if (entitySecret.length != 32) {
        throw new BadRequestException(
          'Invalid entity secret length. Expected 32 bytes.',
        );
      }

      let publicKeyString = this.configService.getOrThrow(
        'CIRCLE_GENERATED_PUBLIC_KEY',
      );

      // encrypt data by the public key
      const publicKey = forge.pki.publicKeyFromPem(publicKeyString);
      const encryptedData = publicKey.encrypt(entitySecret, 'RSA-OAEP', {
        md: forge.md.sha256.create(),
        mgf1: {
          md: forge.md.sha256.create(),
        },
      });

      // encode to base64
      const base64EncryptedData = forge.util.encode64(encryptedData);

      return {
        success: true,
        ciphertext: base64EncryptedData,
        message: 'Entity secret ciphertext generated successfully',
      };
    } catch (error) {
      console.error('Error generating entity secret ciphertext:', error);
      if (error instanceof Error) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  private async generateEnSecreteAndRegister(): Promise<string> {
    try {
      const recoveryDir = process.cwd();
      //this register your Entity Secret.
      const response = await registerEntitySecretCiphertext({
        apiKey: this.configService.getOrThrow('CIRCLE_API_KEY'),
        entitySecret: this.configService.getOrThrow('CIRCLE_ENTITY_SECRET'),
        recoveryFileDownloadPath: recoveryDir,
      });
      // Save recovery file manually (optional)
      if (response.data?.recoveryFile) {
        writeFileSync(
          join(recoveryDir, 'recovery_file.dat'),
          response.data.recoveryFile,
        );
      }

      return '✅ Entity registered successfully';
    } catch (error) {
      console.log({ error });
      if (error instanceof Error) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }
}
