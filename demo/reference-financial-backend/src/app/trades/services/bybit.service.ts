import { BadRequestException, Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { AxiosError } from 'axios';
import {
  AmendOrderParamsV5,
  BatchAmendOrderParamsV5,
  BatchCancelOrderParamsV5,
  BatchOrderParamsV5,
  CancelAllOrdersParamsV5,
  CancelOrderParamsV5,
  CategoryV5,
  GetAccountHistoricOrdersParamsV5,
  OrderParamsV5,
  RestClientV5,
} from 'bybit-api';

@Injectable()
export class BybitService {
  constructor(private readonly configService: ConfigService) {}

  async amendOrder(payload: AmendOrderParamsV5) {
    try {
      const client = this.bybitClient();
      return client.amendOrder(payload);
    } catch (error) {
      if (error instanceof AxiosError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  async placeOrder(payload: OrderParamsV5) {
    try {
      const client = this.bybitClient();
      return client.submitOrder(payload);
    } catch (error) {
      if (error instanceof AxiosError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  // async submitLimitOrder(payload: OrderParamsV5) {
  //   try {
  //     const client = this.bybitClient();
  //     return client.submitOrder(payload);
  //   } catch (error) {
  //     if (error instanceof AxiosError) {
  //       throw new BadRequestException(error.message);
  //     }
  //     throw error;
  //   }
  // }

  async cancelOrder(payload: CancelOrderParamsV5) {
    try {
      const client = this.bybitClient();
      return client.cancelOrder(payload);
    } catch (error) {
      if (error instanceof AxiosError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  async openAndCloseOrder(payload: GetAccountHistoricOrdersParamsV5) {
    try {
      const client = this.bybitClient();
      return client.getActiveOrders(payload);
    } catch (error) {
      if (error instanceof AxiosError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  async cancelAllOrders(payload: CancelAllOrdersParamsV5) {
    try {
      const client = this.bybitClient();
      return client.cancelAllOrders(payload);
    } catch (error) {
      if (error instanceof AxiosError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  async placeBatchOrder(category: CategoryV5, payload: BatchOrderParamsV5[]) {
    try {
      const client = this.bybitClient();
      return await client.batchSubmitOrders(category, payload);
    } catch (error) {
      if (error instanceof AxiosError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  async amendBatchOrder(
    category: CategoryV5,
    payload: BatchAmendOrderParamsV5[],
  ) {
    try {
      const client = this.bybitClient();
      return client.batchAmendOrders(category, payload);
    } catch (error) {
      if (error instanceof AxiosError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  async batchCancel(category: CategoryV5, payload: BatchCancelOrderParamsV5[]) {
    try {
      const client = this.bybitClient();
      return client.batchCancelOrders(category, payload);
    } catch (error) {
      if (error instanceof AxiosError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  async balance() {
    try {
      const client = this.bybitClient();
      return client.getWalletBalance({
        accountType: 'UNIFIED',
      });
    } catch (error) {
      if (error instanceof AxiosError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  async getInstrumentsInfo(symbol: string, category: CategoryV5 = 'spot') {
    try {
      const client = this.bybitClient();
      return client.getInstrumentsInfo({
        category: category,
        symbol: symbol,
      });
    } catch (error) {
      if (error instanceof AxiosError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  async getCurrentPrice(
    symbol: string,
    category: 'linear' | 'inverse',
  ): Promise<number> {
    try {
      const client = this.bybitClient();
      const response = await client.getTickers({
        category: category,
        symbol: symbol,
      });
      if (response.retCode === 0) {
        const lastPrice = response.result.list[0].lastPrice;
        console.log(`Current price for ${symbol}: ${lastPrice}`);
        return parseFloat(lastPrice);
      } else {
        console.error('Error fetching price:', response.retMsg);
        throw new BadRequestException(
          `Error fetching price: ${response.retMsg}`,
        );
      }
    } catch (error) {
      if (error instanceof AxiosError) {
        throw new BadRequestException(error.message);
      }
      console.error('API call failed:', error);
      throw error;
    }
  }

  private bybitClient() {
    return new RestClientV5({
      key: this.configService.getOrThrow('BYBIT_API_KEY'),
      secret: this.configService.getOrThrow('BYBIT_SECRET_KEY'),
      baseUrl: this.configService.getOrThrow('BYBIT_BASE_URI'),
      recv_window: 5000,
      enable_time_sync: true,
    });
  }
}
