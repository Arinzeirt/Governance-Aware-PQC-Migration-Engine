import { AuthUser } from '@app/common';
import {
  ForbiddenException,
  Injectable,
  NotFoundException,
} from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import Big from 'big.js';
import { endOfWeek, startOfWeek } from 'date-fns';
import { Between, DataSource, In, Not, Repository } from 'typeorm';
import { CopySettingEntity, Trades } from '../entities';
import { copyTrading, status, type } from '../input';
import { TradeDefineService } from './define.service';
import { v4 as uuidv4 } from 'uuid';
import { BybitService } from './bybit.service';
import { SubscriptionService } from '@app/subscription/service';
import { SubscriptionStatus } from '@app/subscription/input';
import { PaymentService } from '@app/services';
import { category } from '@app/wallets/input';
import { EventEmitter2 } from '@nestjs/event-emitter';
import { User } from '@app/users/entity';

@Injectable()
export class CopierTradeService {
  constructor(
    @InjectRepository(Trades) private readonly tradeRepo: Repository<Trades>,
    @InjectRepository(CopySettingEntity)
    private readonly copyTradeSettingsRepo: Repository<CopySettingEntity>,

    private readonly ds: TradeDefineService,
    private readonly subscription: SubscriptionService,
    private readonly bybitService: BybitService,
    private readonly paymentService: PaymentService,
    private readonly datasource: DataSource,
    private readonly eventEmitter: EventEmitter2,
  ) {}

  async CopyTrade(dto: copyTrading, user: AuthUser): Promise<Trades> {
    const trade = await this.tradeRepo.findOne({
      where: { id: dto.tradeId },
    });

    if (!trade) throw new NotFoundException('Trade not found');

    const copySetting = await this.copyTradeSettingsRepo.findOne({
      where: { trader: { id: trade.creatorId }, user: { id: user.id } },
    });

    let amount = dto.amount;
    if (copySetting) {
      if (copySetting.copyMode === 'Proportional') {
        amount = trade.margin * copySetting.copyRatio;
      } else {
        amount = copySetting.amount;
      }
    } else if (!dto.amount) {
      amount = trade.margin;
    }

    // find if the user account is on subscription if not the user can only copy five trade per week
    const activeSubscription =
      await this.subscription.getActiveSubscription(user);

    let userSubscription = false;
    if (activeSubscription) {
      userSubscription =
        activeSubscription.status === SubscriptionStatus.active;
    }

    const current = new Date();
    const start = startOfWeek(current, { weekStartsOn: 1 });
    const end = endOfWeek(current, { weekStartsOn: 1 });

    if (!userSubscription) {
      const weeklyCopy = await this.tradeRepo.find({
        where: { userId: user.id, createdAt: Between(start, end) },
      });

      if (weeklyCopy.length >= 5) {
        throw new ForbiddenException('Weekly trade copied exhausted');
      }
    }

    // const payment = await this.paymentService.internalDebitUser({
    //   user,
    //   amount,
    //   category: category.trade,
    // });

    console.log(trade.symbol);
    const currentPrice = await this.bybitService.getCurrentPrice(
      trade.symbol,
      'linear',
    );

    return this.datasource.manager.transaction(async (manager) => {
      // Lock the original trade row for update
      const lockedTrade = await manager.findOne(Trades, {
        where: { id: dto.tradeId, status: Not(status.close) },
        lock: { mode: 'pessimistic_write' },
      });

      if (!lockedTrade) throw new NotFoundException('Trade not found');

      // Check if user already copied this trade (by identifier)
      const isUserHaveSameTrade = await manager.findOne(Trades, {
        where: {
          identifier: lockedTrade.identifier,
          userId: user.id,
          status: Not(In([status.close, status.fail])),
        },
      });

      if (isUserHaveSameTrade) {
        throw new ForbiddenException('Same trade already executed');
      }

      lockedTrade.noOfCopiers = Big(lockedTrade.noOfCopiers)
        .plus(Big(1))
        .toNumber();

      const identifier = lockedTrade.identifier;
      const trade = this.ds.handleTraderDuration(lockedTrade, identifier);

      const save = manager.create(Trades, {
        ...trade,
        id: uuidv4(),
        userId: user.id,
        currentPrice,
        tradeType: type.copy,
        positionSize: {
          amount,
          currency: 'USDT',
        },
        // fundId: payment?.id,
        status: status.pending,
        orderLinkId: uuidv4(),
      });

      const newTrade = await manager.save(save);
      await manager.update(
        Trades,
        { identifier: lockedTrade.identifier },
        {
          currentPrice,
          noOfCopiers: lockedTrade.noOfCopiers,
        },
      );

      const findUser = await manager.findOne(User, { where: { id: user.id } });
      if (findUser && !findUser.quickStart.firstTrade) {
        findUser.quickStart.firstTrade = true;
        await manager.save(findUser);
      }

      // TODO when we uncomment the payment service
      this.eventEmitter.emit('execute.trade', {
        tradeId: newTrade.id,
        // fundId: newTrade.fundId,
      });
      return newTrade;
    });
  }
}
