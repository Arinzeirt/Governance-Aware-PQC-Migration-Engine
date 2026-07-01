import {
  BadRequestException,
  ForbiddenException,
  Injectable,
} from '@nestjs/common';
import {
  cache,
  convert,
  convertResponse,
  fetchRatesResponse,
  fiatRatesResponse,
  usdcResponse,
} from '../input';
import Big from 'big.js';
import { HttpClientService } from '@app/services';
import { AxiosError } from 'axios';

@Injectable()
export class ConvertDefineService {
  private readonly coingeckoBase = 'https://api.coingecko.com/api/v3';
  private readonly fiatUrl = 'https://open.er-api.com/v6/latest';
  private cache: cache = { timestamp: 0, rates: null };
  private cryptoMap: Record<string, string> = {
    BTC: 'bitcoin',
    ETH: 'ethereum',
    USDT: 'tether',
    USDC: 'usd-coin',
  };

  private fiatCurrencies = ['USD', 'NGN', 'EUR', 'GBP'];

  constructor(protected httpService: HttpClientService) {}

  async getCachedRates(): Promise<fetchRatesResponse> {
    const now = Date.now();
    const cacheValid =
      this.cache.timestamp && now - this.cache.timestamp < 10 * 60 * 1000;

    if (cacheValid && this.cache.rates) return this.cache.rates;

    const rates = await this.fetchRates();
    this.cache = { timestamp: now, rates };
    return rates;
  }

  public convertFromRates(
    dto: convert,
    rates: fetchRatesResponse,
  ): convertResponse {
    const { fiatRates, cryptoRates } = rates;
    const fromUsd = this.getUsdValue(dto.from, fiatRates, cryptoRates);
    const toUsd = this.getUsdValue(dto.to, fiatRates, cryptoRates);
    const converted = Big(dto.amount)
      .times(Big(fromUsd))
      .div(Big(toUsd))
      .toFixed(6);

    return {
      amount: dto.amount,
      from: dto.from,
      to: dto.to,
      converted: Number(converted),
      rate: Number(Big(fromUsd).div(Big(toUsd)).toFixed(6)),
    };
  }

  public getUsdValue(
    symbol: string,
    fiatRates: fiatRatesResponse,
    cryptoPrices: usdcResponse,
  ): number {
    symbol = symbol.toUpperCase();

    if (this.fiatCurrencies.includes(symbol)) {
      return 1 / (fiatRates.rates[symbol] || (symbol === 'USD' ? 1 : 0));
    }

    // if (symbol === 'STP') {
    //   // 1000 STP = 1 USD → 1 STP = 0.001 USD
    //   return 0.001;
    // }

    if (symbol === 'STP') {
      // 1000 STP = 10 USD → 1 STP = 0.01 USD
      return 0.01;
    }

    const cryptoId = this.cryptoMap[symbol];
    if (cryptoId && cryptoPrices[cryptoId]) {
      return cryptoPrices[cryptoId].usd;
    }

    throw new ForbiddenException(`Unsupported currency: ${symbol}`);
  }

  async fetchRates(): Promise<fetchRatesResponse> {
    try {
      const [fiatRes, cryptoRes] = await Promise.all([
        this.httpService.get<fiatRatesResponse>({
          uri: `${this.fiatUrl}/USD`,
        }),

        this.httpService.get<usdcResponse>({
          uri: `${this.coingeckoBase}/simple/price`,
          params: {
            ids: Object.values(this.cryptoMap).join(','),
            vs_currencies: 'usd,ngn',
          },
        }),
      ]);

      const fiatRates = fiatRes.data;
      const cryptoRates = cryptoRes.data;

      return { fiatRates, cryptoRates };
    } catch (error) {
      if (error instanceof AxiosError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }
}
