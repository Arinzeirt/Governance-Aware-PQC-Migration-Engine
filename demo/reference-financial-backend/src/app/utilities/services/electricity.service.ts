/* eslint-disable @typescript-eslint/no-unused-vars */
import {
  BadRequestException,
  ForbiddenException,
  Injectable,
} from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { AxiosError } from 'axios';
import {
  billType,
  electricityPayload,
  metercode,
  verifyMeterName,
  verifyResponse,
} from '../input';
import { DefineService } from './define.service';
import { AuthUser } from '@app/common';
import { category } from '@app/wallets/input';
import { HttpClientService } from '@app/services';
import { v4 as uuidv4 } from 'uuid';

@Injectable()
export class ElectricityService {
  constructor(
    private readonly httpService: HttpClientService,
    private readonly ds: DefineService,
    private readonly configService: ConfigService,
  ) {}

  public electricityCompanies() {
    const electCompanies = [
      { name: 'Ikeja Electricity', code: metercode.ikeja, short: 'IKEDC' },
      { name: 'Eko Electricity', code: metercode.eko, short: 'EKEDC' },
      { name: 'Kano Electricity', code: metercode.kano, short: 'KEDCO' },
      {
        name: 'Port Harcourt Electricity',
        code: metercode.port,
        short: 'PHED',
      },
      { name: 'Jos Electricity', code: metercode.jos, short: 'JED' },
      { name: 'Ibadan Electricity', code: metercode.ibadan, short: 'IBEDC' },
      { name: 'Kaduna Electricity', code: metercode.kaduna, short: 'KAEDCO' },
      { name: 'Abuja Electricity', code: metercode.abuja, short: 'AEDC' },
      { name: 'Enugu Electricity', code: metercode.enugu, short: 'EEDC' },
      { name: 'Benin Electricity', code: metercode.benin, short: 'BEDC' },
      { name: 'Aba Electricity', code: metercode.aba, short: 'ABA' },
      { name: 'Yola Electricity', code: metercode.yola, short: 'YEDC' },
    ];

    return electCompanies;
  }

  async verifyMeterNumber(payload: verifyMeterName): Promise<verifyResponse> {
    try {
      const response = await this.httpService.post<verifyResponse>({
        uri: `${this.configService.getOrThrow('VTPASS_URI')}/merchant-verify`,
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

  async ElectricityPurchase(payload: electricityPayload, user: AuthUser) {
    try {
      const { pin, idempotency, type, ...rest } = payload;

      const isMatch = await this.ds.checkedPin(pin, user);
      if (!isMatch) throw new BadRequestException('Incorrect transaction pin');

      const verify = await this.verifyMeterNumber({
        billersCode: rest.billersCode,
        serviceID: rest.serviceID,
        type: type,
      });

      const company = this.electricityCompanies();
      const cd = company.find((d) => d.code === rest.serviceID);

      if (verify.code !== '000' || !cd) {
        throw new ForbiddenException('unable to verify customer name');
      }

      rest.request_id = uuidv4();
      rest.variation_code = type;
      const result = await this.ds.handlePayment(
        {
          amount: payload.amount,
          idempotency: payload.idempotency,
          service: category.electricity,
        },
        user,
        {
          type: type,
          payload: rest,
          category: billType.electricity,
          customerName: verify.content.Customer_Name,
        },
      );

      if (result.alreadyProcessed) return result;

      return result;
    } catch (error) {
      if (error instanceof AxiosError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }
}
