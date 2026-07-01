/* eslint-disable @typescript-eslint/no-unused-vars */
import { AuthUser } from '@app/common';
import { MailService, PaymentService, template } from '@app/services';
import { functionRetry, google } from '@app/utils';
import {
  BadRequestException,
  ForbiddenException,
  forwardRef,
  Inject,
  Injectable,
} from '@nestjs/common';
import { EventEmitter2 } from '@nestjs/event-emitter';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository, TypeORMError } from 'typeorm';
import { v4 as uuidv4 } from 'uuid';
import {
  AiTradeInputSchema,
  AiTradeOutputSchema,
  PromptTemplate,
} from '../config';
import { Trades } from '../entities';
import {
  createTrade,
  duration,
  orderType,
  riskLevel,
  status,
  type,
} from '../input';
import { BybitService } from './bybit.service';
import { TradeDefineService } from './define.service';
import { ActivityService } from './activities.service';

@Injectable()
export class CreateTradeService {
  constructor(
    @InjectRepository(Trades)
    private readonly tradeRepository: Repository<Trades>,
    @Inject(forwardRef(() => TradeDefineService))
    private readonly ds: TradeDefineService,
    private readonly activityFeed: ActivityService,
    private readonly bybitService: BybitService,
    private readonly paymentService: PaymentService,
    private readonly eventEmitter: EventEmitter2,
    private readonly mailService: MailService,
  ) {}

  async createNewTrade(payload: createTrade, user: AuthUser): Promise<Trades> {
    try {
      // const duplicate = await this.tradeRepository.findOne({
      //   where: {
      //     asset: payload.asset,
      //     creatorId: user.id,
      //     action: payload.action,
      //     status: Not(In([status.close, status.draft])),
      //   },
      // });
      // if (duplicate) {
      //   return duplicate;
      // }

      const now = new Date();
      const symbol = this.extractSymbol(payload.asset);
      const identifier = uuidv4();

      if (payload.orderType === orderType.market) {
        const currentPrice = await this.currentPrice(payload.asset);

        if (currentPrice === undefined) {
          throw new BadRequestException('Unable to fetch current market price');
        }

        payload.entryPrice = currentPrice;
      }

      payload = this.ds.handleTraderDuration(payload, identifier);

      let tradeStatus;
      let sendFund;
      if (payload.isDraft) {
        tradeStatus = status.draft;
      } else if (
        payload.duration === duration.custom &&
        payload.startDate &&
        payload.startDate > now
      ) {
        tradeStatus = status.schedule;
      } else {
        // sendFund = await this.paymentService.processChargeOnUser({
        //   user: user,
        //   amount: payload.positionSize.amount,
        //   category: category.trade,
        //   symbol,
        // });
        tradeStatus = status.pending;
      }

      payload.riskLevel = this.calculateRisk(payload.leverage);

      const tradeObject = {
        ...payload,
        identifier,
        symbol,
        tradeType: type.original,
        status: tradeStatus,
        userId: user.id,
        creatorId: user.id,
        orderLinkId: uuidv4(),
        margin: payload.positionSize.amount,
        // fundId: sendFund?.id,
      };

      const newTrade = await this.tradeRepository.save(
        this.tradeRepository.create(tradeObject),
      );
      // if (!payload.isDraft) {
      //   this.tradeJW.sendNotificationToFollowers({
      //     creatorId: user.id,
      //     tradeId: newTrade.id,
      //   });
      // }
      void this.activityFeed.create({
        title: `Trade ${payload.isDraft ? 'Drafted' : 'Published'} `,
        message: `${payload.asset} trade ${payload.isDraft ? 'Drafted' : 'Published'} - Entry: ${payload.entryPrice?.toLocaleString()} | SL: ${payload.stopLoss.toLocaleString()} | PT: ${payload.takeProfit.toLocaleString()}`,
        userId: user.id,
      });

      // TODO when we uncomment the payment service
      this.eventEmitter.emit('execute.trade', {
        tradeId: newTrade.id,
        // fundId: newTrade.fundId,
      });

      this.AiTradeSummarizer(newTrade);
      this.mailService.sendMail(
        user.email,
        template.tradePending,
        'Trade Submitted and it is Pending',
        {
          fullName: user.username || 'Trader',
        },
      );
      return newTrade;
    } catch (error) {
      if (error instanceof TypeORMError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  async checkTradeStatus(id: string) {
    const data = await this.bybitService.openAndCloseOrder({
      category: 'linear',
      orderId: id,
    });

    return data;
  }

  async editTrade(id: string, payload: Partial<createTrade>, user: AuthUser) {
    const trade = await this.tradeRepository.findOne({
      where: { id },
    });
    if (!trade) throw new BadRequestException('Trade not found');

    if (trade.userId !== user.id) {
      throw new ForbiddenException('You are not authorized to edit this trade');
    }

    if (trade.status === status.draft) {
      const updatedTrade = await this.tradeRepository.save({
        ...trade,
        ...payload,
      });
      return updatedTrade;
    }

    let editOnBybit;
    if (trade.orderType === orderType.market) {
      editOnBybit = await this.bybitService.amendOrder({
        category: 'linear',
        orderId: trade.orderLinkId,
        symbol: trade.symbol,
      });
    }
  }

  async currentPrice(symbol: string) {
    const sym = this.extractSymbol(symbol);
    const currentPrice = await this.bybitService.getCurrentPrice(sym, 'linear');
    return currentPrice;
  }

  private extractSymbol(symbol: string) {
    const first = symbol.split('/')[0];
    const second = symbol.split('/')[1];
    return `${first}${second}`.toUpperCase();
  }

  private calculateRisk(leverage: number) {
    if (leverage <= 4) return riskLevel.low;
    if (leverage <= 9) return riskLevel.medium;
    return riskLevel.high;
  }

  private async AiTradeSummarizer(trade: Trades): Promise<void> {
    const aiTrade = google.defineFlow(
      {
        name: `ai-trade-flow-${trade.id}`,
        inputSchema: AiTradeInputSchema,
        outputSchema: AiTradeOutputSchema,
      },
      async (input) => {
        try {
          return await functionRetry(
            async () => {
              const { output } = await PromptTemplate({ tradeData: input });
              return output;
            },
            5,
            20000,
          );
        } catch (error) {
          console.error('AI Trade Summarizer Error:', error);
          throw error;
        }
      },
    );
    const response = await aiTrade({
      ...trade,
      startDate: trade.startDate?.toISOString(),
      expiresAt: trade.expiresAt?.toISOString(),
      createdAt: trade.createdAt?.toISOString(),
      updatedAt: trade.updatedAt?.toISOString(),
    });

    // console.log(response);
    await this.tradeRepository.update(trade.id, {
      ...response,
    });
    return;
  }
}
