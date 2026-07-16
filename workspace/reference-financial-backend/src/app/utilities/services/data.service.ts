/* eslint-disable @typescript-eslint/no-unused-vars */
import { AuthUser } from '@app/common';
import { HttpClientService } from '@app/services';
import { category } from '@app/wallets/input';
import {
  BadRequestException,
  ForbiddenException,
  Injectable,
} from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { AxiosError, AxiosResponse } from 'axios';
import { billType, dataResponse, getData, IData, varations } from '../input';
import { DefineService } from './define.service';
import { v4 as uuidv4 } from 'uuid';

@Injectable()
export class DataService {
  constructor(
    private readonly httpService: HttpClientService,
    private readonly defineService: DefineService,
    private readonly configService: ConfigService,
  ) {}

  async getAvailableData(payload: getData): Promise<dataResponse> {
    try {
      const response: AxiosResponse<dataResponse> =
        await this.httpService.get<dataResponse>({
          uri: `${this.configService.getOrThrow('VTPASS_URI')}/service-variations?serviceID=${payload.code}`,
          headers: {
            'api-key': this.configService.getOrThrow('VTPASS_API_KEY'),
            'public-key': this.configService.getOrThrow('VTPASS_PUBLIC_KEY'),
          },
        });

      return this.formatDataResponse(response);
    } catch (error) {
      if (error instanceof AxiosError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  async dataPurchase(payload: IData, user: AuthUser) {
    try {
      const { pin, idempotency, networkCode, phone, ...rest } = payload;

      const isMatch = await this.defineService.checkedPin(pin, user);
      if (!isMatch) {
        throw new BadRequestException('Incorrect transaction pin');
      }

      const bundle = await this.getAvailableData({ code: networkCode });
      if (bundle.response_description !== '000')
        throw new ForbiddenException('Unable to verify product');
      let product: varations;

      const varation: varations | undefined = bundle.content.varations.find(
        (d: varations) => d.variation_code === payload.variation_code,
      );

      if (varation) {
        product = varation;
      } else {
        const variations: varations | undefined =
          bundle.content.variations.find(
            (d: varations) => d.variation_code === payload.variation_code,
          );

        if (!variations) {
          throw new ForbiddenException(
            'Selected product is not available at the moment',
          );
        }

        product = variations;
      }

      rest.billersCode = phone;
      rest.amount = product.variation_amount;
      rest.request_id = uuidv4();
      const result = await this.defineService.handlePayment(
        {
          amount: parseFloat(product.variation_amount),
          idempotency: payload.idempotency,
          service: category.data,
        },
        user,
        {
          payload: rest,
          category: billType.data,
          type: product.name,
          bundleSize: product.bundleSize,
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

  private formatDataResponse(response: AxiosResponse<dataResponse>) {
    const data = response.data;

    const mapVar = (v: varations) => ({
      ...v,
      bundleSize: this.extractBundleSize(v?.name || ''),
      duration: this.extractDuration(v?.name || ''),
    });

    const content: any = { ...data.content };

    if (Array.isArray(content.variations)) {
      content.variations = content.variations.map(mapVar);
    }
    if (Array.isArray(content.varations)) {
      content.varations = content.varations.map(mapVar);
    }

    return {
      ...data,
      content,
    };
  }

  private extractBundleSize(name: string): string | undefined {
    if (!name) return undefined;
    const sizeMatch = name.match(/(\d+(?:\.\d+)?)\s*(KB|MB|GB|TB)\b/i);
    if (sizeMatch) {
      const value = sizeMatch[1];
      const unit = sizeMatch[2].toUpperCase();
      return `${value}${unit}`;
    }
    return undefined;
  }

  private extractDuration(name: string): string | undefined {
    if (!name) return undefined;

    // e.g., "24 hrs", "2 days", "1 Month", "2-Month", "1 Year"
    const numUnit = name.match(
      /(\d+(?:\.\d+)?)\s*[- ]?\s*(hrs?|hours?|days?|weeks?|months?|years?)/i,
    );
    if (numUnit) {
      const value = numUnit[1];
      const unitRaw = numUnit[2].toLowerCase();
      const unit = /hr|hour/.test(unitRaw)
        ? 'hours'
        : /day/.test(unitRaw)
          ? 'days'
          : /week/.test(unitRaw)
            ? 'weeks'
            : /month/.test(unitRaw)
              ? 'months'
              : /year/.test(unitRaw)
                ? 'years'
                : unitRaw;
      return `${value} ${unit}`;
    }

    // Parenthetical durations e.g., "( 1 Month )"
    const paren = name.match(
      /\(\s*(\d+(?:\.\d+)?)\s*(hrs?|hours?|days?|weeks?|months?|years?)\s*\)/i,
    );
    if (paren) {
      const value = paren[1];
      const unitRaw = paren[2].toLowerCase();
      const unit = /hr|hour/.test(unitRaw)
        ? 'hours'
        : /day/.test(unitRaw)
          ? 'days'
          : /week/.test(unitRaw)
            ? 'weeks'
            : /month/.test(unitRaw)
              ? 'months'
              : /year/.test(unitRaw)
                ? 'years'
                : unitRaw;
      return `${value} ${unit}`;
    }

    // Wordy durations like "Weekly", "Monthly", "Yearly", "Daily"
    const wordy = name.match(/\b(daily|weekly|monthly|yearly)\b/i);
    if (wordy) {
      const w = wordy[1].toLowerCase();
      const map: Record<string, string> = {
        daily: '1 day',
        weekly: '1 week',
        monthly: '1 month',
        yearly: '1 year',
      };
      return map[w];
    }

    // Hyphen forms e.g., "2-Month Plan"
    const hyphenForm = name.match(
      /(\d+(?:\.\d+)?)\s*-\s*(month|months|week|weeks|year|years|day|days)/i,
    );
    if (hyphenForm) {
      const value = hyphenForm[1];
      const unitRaw = hyphenForm[2].toLowerCase();
      const unit = /day/.test(unitRaw)
        ? 'days'
        : /week/.test(unitRaw)
          ? 'weeks'
          : /month/.test(unitRaw)
            ? 'months'
            : /year/.test(unitRaw)
              ? 'years'
              : unitRaw;
      return `${value} ${unit}`;
    }

    return undefined;
  }
}
