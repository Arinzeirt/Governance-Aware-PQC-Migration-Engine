import { AuthUser } from '@app/common';
import { HttpClientService } from '@app/services';
import {
  BadRequestException,
  ForbiddenException,
  Injectable,
} from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { FiatAccount } from '../entities';
import { User } from '@app/users/entity';
import { Repository } from 'typeorm';
import { InjectRepository } from '@nestjs/typeorm';
import { nanoid } from 'nanoid';
import {
  getEncryptedData,
  initialFundTransfer,
  signatureResponse,
  transferFunds,
  virtualAccountResponse,
} from '../input';
import { AxiosError } from 'axios';
import { getOtpResponse, nameEnquiry } from '../input';
import { v4 as uuidV4 } from 'uuid';

@Injectable()
export class SeerBitService {
  constructor(
    @InjectRepository(FiatAccount)
    private readonly accountRepo: Repository<FiatAccount>,
    @InjectRepository(User)
    private readonly userRepo: Repository<User>,
    private readonly httpClient: HttpClientService,
    private readonly configService: ConfigService,
  ) {}

  async createVirtualAccount(data: string | AuthUser): Promise<FiatAccount> {
    try {
      const user: AuthUser =
        typeof data === 'string' ? (JSON.parse(data) as AuthUser) : data;

      const findUser = await this.userRepo.findOne({ where: { id: user.id } });
      if (!findUser) throw new ForbiddenException('User not found');

      const haveNairaAccount = await this.accountRepo.findOne({
        where: { userId: user.id },
      });

      if (haveNairaAccount) return haveNairaAccount;

      const reference = nanoid(10);
      const response = await this.httpClient.post<virtualAccountResponse>({
        uri: 'https://seerbitapi.com/api/v2/virtual-accounts',
        body: {
          publicKey: this.configService.getOrThrow('SEERBIT_PUBLIC_API'),
          fullName: findUser.fullName,
          bankVerificationNumber: '',
          currency: 'NGN',
          country: 'NG',
          reference,
          email: findUser.email,
        },
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${this.configService.getOrThrow('SEERBIT_ENCRYPTED_KEY')}`,
        },
      });

      if (response.status !== 'SUCCESS') {
        throw new BadRequestException('Error creating virtual account');
      }

      const createAccount = this.accountRepo.create({
        ...response.data.payments,
        userId: user.id,
        user: findUser,
      });

      return this.accountRepo.save(createAccount);
    } catch (error) {
      if (error instanceof AxiosError) {
        throw new ForbiddenException(error.message);
      }
      throw error;
    }
  }

  async nameEnquiry(payload: nameEnquiry) {
    try {
      const data = await this.httpClient.post({
        uri: 'https://pocket.seerbitapi.com/pocket/payout/account-enquiry',
        body: payload,
        headers: {
          Authorization: `Bearer ${this.configService.getOrThrow('SEERBIT_ENCRYPTED_KEY')}`,
        },
      });
      console.log(data);
      return data;
    } catch (error) {
      if (error instanceof AxiosError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  async bankList() {
    try {
      const { data } = await this.httpClient.get({
        uri: 'https://pocket.seerbitapi.com/pocket/banks',
        headers: {
          Authorization: `Bearer ${this.configService.getOrThrow('SEERBIT_ENCRYPTED_KEY')}`,
          'Public-Key': `${this.configService.getOrThrow('SEERBIT_PUBLIC_API')}`,
        },
      });
      console.log(data);

      return data;
    } catch (error) {
      if (error instanceof AxiosError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  async TransferFund(payload: transferFunds) {
    try {
      const { transactionPin, ...rest } = payload;
      console.log(transactionPin);
      const response = await this.generateSignature(rest);
      const request = await this.httpClient.post<initialFundTransfer>({
        uri: `https://pocket.seerbitapi.com/pocket/payout/encrypted/pocket-id/${this.configService.getOrThrow('POCKETID')}`,
        body: { ...response.input, signature: response.data.signature },
        headers: {
          Authorization: `Bearer ${this.configService.getOrThrow('SEERBIT_ENCRYPTED_KEY')}`,
        },
      });

      console.log(request);
      return request;
    } catch (error) {
      if (error instanceof AxiosError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  private async generateOTP() {
    try {
      const response = await this.httpClient.post<getOtpResponse>({
        uri: 'https://pocket.seerbitapi.com/pocket/getOtp',
        body: {
          actionItem: 'APPROVE_DISBURSEMENT',
          pocketId: 'your_pocket_id_here',
        },
        headers: {
          Authorization: `Bearer ${this.configService.getOrThrow('SEERBIT_ENCRYPTED_KEY')}`,
        },
      });
      console.log(response);
      return response;
    } catch (error) {
      if (error instanceof AxiosError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  private async generateSignature(payload: transferFunds) {
    try {
      const { data } = await this.generateOTP();

      if (!payload.reference) payload.reference = uuidV4();
      payload.currency = 'NGN';
      payload.actionType = data.category;
      payload.passKey = data.otp;

      const response = await this.httpClient.post<signatureResponse>({
        uri: 'https://pocket.seerbitapi.com/pocket/payout/get-signature',
        body: payload,
        headers: {
          Authorization: `${this.configService.getOrThrow('SEERBIT_ENCRYPTED_KEY')}`,
        },
      });
      console.log(response);
      return { ...response, input: payload };
    } catch (error) {
      if (error instanceof AxiosError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  private async getEncryptedKey() {
    try {
      const response = await this.httpClient.post<getEncryptedData>({
        uri: 'https://seerbitapi.com/api/v2/virtual-accounts',
        body: {
          key: `${this.configService.getOrThrow('SEERBIT_PRIVATE_API')}.${this.configService.getOrThrow('SEERBIT_PUBLIC_API')}`,
        },
        headers: {
          'Content-Type': 'application/json',
        },
      });
      return response;
    } catch (error) {
      if (error instanceof AxiosError) {
        throw new ForbiddenException(error.message);
      }
      throw error;
    }
  }
}
