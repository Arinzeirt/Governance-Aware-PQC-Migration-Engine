/* eslint-disable @typescript-eslint/no-unused-vars */
import { AuthUser } from '@app/common';
import { category } from '@app/wallets/input';
import {
  BadRequestException,
  Injectable,
  InternalServerErrorException,
} from '@nestjs/common';
import { TypeORMError } from 'typeorm';
import { v4 as uuidV4 } from 'uuid';
import { billType, IAirtime } from '../input';
import { DefineService } from './define.service';

@Injectable()
export class AirtimeService {
  constructor(private readonly ds: DefineService) {}

  async AirtimePurchase(payload: IAirtime, user: AuthUser) {
    try {
      const { pin, idempotency, ...rest } = payload;

      const isMatch = await this.ds.checkedPin(pin, user);
      if (!isMatch) {
        throw new BadRequestException('Incorrect transaction pin');
      }

      rest.request_id = uuidV4();
      const result = await this.ds.handlePayment(
        {
          amount: rest.amount,
          idempotency: payload.idempotency,
          service: category.airtime,
        },
        user,
        { category: billType.airtime, payload: rest, type: 'direct' },
      );

      if (result.alreadyProcessed) return result;
      return result;
    } catch (error) {
      if (error instanceof TypeORMError) {
        throw new InternalServerErrorException();
      }
      throw error;
    }
  }
}
