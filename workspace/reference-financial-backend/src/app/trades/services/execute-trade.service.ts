import {
  BadRequestException,
  forwardRef,
  Inject,
  Injectable,
} from '@nestjs/common';
import { OnEvent } from '@nestjs/event-emitter';
import { InjectRepository } from '@nestjs/typeorm';
import Big from 'big.js';
import { endOfDay, startOfDay } from 'date-fns';
import { Between, Repository } from 'typeorm';
import { Trades } from '../entities';
import { orderType, placeTrade, quality, status } from '../input';
import { BybitService } from './bybit.service';
import { TradeJobWorker } from './trade-schedule.service';
import { MailService, template } from '@app/services';
import { ConfigService } from '@nestjs/config';

@Injectable()
export class ExecuteTradeService {
  constructor(
    @InjectRepository(Trades)
    private readonly tradeRepository: Repository<Trades>,
    private readonly bybitService: BybitService,
    private readonly mailService: MailService,
    private readonly configService: ConfigService,

    @Inject(forwardRef(() => TradeJobWorker))
    private readonly tradingJW: TradeJobWorker,
  ) {}

  @OnEvent('execute.trade', { async: true })
  async handleTradeExecution(payload: placeTrade) {
    try {
      const current = new Date();
      const start = startOfDay(current);
      const end = endOfDay(current);

      const trade = await this.tradeRepository.findOne({
        where: {
          id: payload.tradeId,
          // fundId: payload.fundId,
          status: status.pending,
          createdAt: Between(start, end),
        },
        relations: ['user'],
      });

      if (!trade) return;

      const instruments = await this.bybitService.getInstrumentsInfo(
        trade.symbol,
        'linear',
      );

      const currentPrices = await this.bybitService.getCurrentPrice(
        trade.symbol,
        'linear',
      );

      if (!currentPrices || Number(currentPrices) <= 0) {
        throw new BadRequestException(
          'Current price must be a positive number.',
        );
      }

      const tradePrice =
        trade.entryPrice > 0 ? trade.entryPrice : currentPrices;

      const info = instruments.result.list[0];
      const minNotional = 10; // USDT

      const userUsdtAmount = trade.positionSize.amount;
      const qtyStep = Number((info as any).lotSizeFilter.qtyStep);

      const qty = this.normalizeQty({
        userUSDT: userUsdtAmount,
        markPrice: tradePrice,
        minNotionalUSDT: minNotional,
        minOrderQty: Number(info.lotSizeFilter.minOrderQty),
        qtyStep: qtyStep,
        leverage: trade.leverage,
      });

      const type = trade.orderType === orderType.market;
      const executeTrade = await this.bybitService.placeOrder({
        category: 'linear',
        symbol: trade.symbol,
        side: trade.action,
        orderType: type ? 'Market' : 'Limit',
        qty,
        timeInForce: type ? 'IOC' : 'GTC',
        marketUnit: 'quoteCoin',
        positionIdx: 0,
        price: String(tradePrice),
        reduceOnly: false,
        takeProfit: String(trade.takeProfit),
        stopLoss: String(trade.stopLoss),
        orderLinkId: trade.orderLinkId,
        tpslMode: 'Full',
        tpOrderType: 'Market',
        slOrderType: 'Market',
      });

      console.log({ executeTrade });
      const delay = new Date(new Date().setTime(15_000)).getTime();
      if (executeTrade.retCode !== 0) {
        switch (executeTrade.retCode) {
          case 170131:
            // retMsg: 'Insufficient balance.',

            await Promise.all([
              // send a notification to super admin
              this.mailService.sendMail(
                this.configService.getOrThrow('ADMIN_EMAIL'),
                template.bybit,
                'Bybit Trade Execution Failed - Insufficient Balance',
                { accountName: 'Bybit' },
              ),

              this.mailService.sendMail(
                trade.user.email,
                template.tradeFail,
                `${trade.symbol} Trade Execution Failed`,
                {
                  fullName: trade.user.username || 'Trader',
                  reason: executeTrade.retMsg,
                },
              ),
            ]);

            break;

          case 10001:
            // retMsg: 'StopLoss:91650000000 set for Buy position should lower than base_price:89140000000??LastPrice'
            this.mailService.sendMail(
              trade.user.email,
              template.tradeFail,
              `${trade.symbol} Trade Execution Failed`,
              {
                fullName: trade.user.username || 'Trader',
                reason: executeTrade.retMsg,
              },
            );
            break;

          case 110007:
            // retMsg: 'ab not enough for new order'
            await Promise.all([
              // send a notification to super admin
              this.mailService.sendMail(
                this.configService.getOrThrow('ADMIN_EMAIL'),
                template.bybit,
                'Bybit Trade Execution Failed - Insufficient Balance',
                { accountName: 'Bybit' },
              ),

              this.mailService.sendMail(
                trade.user.email,
                template.tradeFail,
                `${trade.symbol} Trade Execution Failed`,
                {
                  fullName: trade.user.username || 'Trader',
                  reason: executeTrade.retMsg,
                },
              ),
            ]);
            break;

          case 10002:
            // retMsg: 'Timestamp for this request is outside of the recvWindow.';
            // handle a schedule to run on 500ms after
            this.tradingJW.reprocessTrading(payload, delay);
            break;

          default:
            // Handle refunds and log error
            this.tradingJW.refundTradePayment(
              {
                userId: trade.userId,
                amount: String(trade.positionSize.amount),
              },
              delay,
            );
            break;
        }
      } else {
        this.mailService.sendMail(
          trade.user.email,
          template.tradeOpen,
          `${trade.symbol} Trade Execution Success`,
          {
            fullName: trade.user.username || 'Trader',
            reason: executeTrade.retMsg,
          },
        );
      }

      trade.errorMsg = this.handleErrorMessage(executeTrade.retMsg);
      trade.orderId = executeTrade.result.orderId;
      trade.currentPrice = currentPrices;
      trade.status = this.handleTradeStatus(executeTrade.retCode);
      trade.orderLinkId = executeTrade.result.orderLinkId;
      await this.tradeRepository.save(trade);
      return;
    } catch (error) {
      if (error instanceof Error) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  private normalizeQty(payload: quality): string {
    const {
      userUSDT,
      markPrice,
      minNotionalUSDT,
      minOrderQty,
      qtyStep,
      leverage,
    } = payload;

    // Validate inputs
    const nums = {
      userUSDT,
      markPrice,
      minNotionalUSDT,
      minOrderQty,
      qtyStep,
      leverage,
    };
    for (const [key, val] of Object.entries(nums)) {
      if (typeof val !== 'number' || isNaN(val) || !isFinite(val)) {
        throw new Error(`Invalid numeric value for ${key}: ${val}`);
      }
    }

    let maxQty = Big(userUSDT).times(leverage).div(markPrice);

    const minNotionalQty = Big(minNotionalUSDT).div(markPrice);

    const exchangeMinQty = minNotionalQty.gt(minOrderQty)
      ? minNotionalQty
      : Big(minOrderQty);

    if (maxQty.lt(exchangeMinQty)) maxQty = exchangeMinQty;

    const roundedQty = Math.floor(maxQty.toNumber() / qtyStep) * qtyStep;

    const finalQty = Math.max(roundedQty, exchangeMinQty.toNumber());

    console.log({ finalQty });
    return new Big(finalQty).toFixed(6);
  }

  private handleTradeStatus = (code: number): status => {
    if (code === 0) return status.open;
    if (code === 10002) return status.pending;
    return status.fail;
  };

  private handleErrorMessage = (message: string): string => {
    const insuf = ['Insufficient balance.', 'ab not enough for new order'];
    if (insuf.includes(message)) return 'process timeout';
    return message;
  };
}
