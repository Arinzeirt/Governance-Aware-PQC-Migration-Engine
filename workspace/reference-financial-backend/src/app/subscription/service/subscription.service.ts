import { AuthUser } from '@app/common';
import { PaymentService } from '@app/services';
import { category } from '@app/wallets/input';
import {
  ForbiddenException,
  forwardRef,
  Inject,
  Injectable,
  Logger,
} from '@nestjs/common';
import { OnEvent } from '@nestjs/event-emitter';
import { InjectRepository } from '@nestjs/typeorm';
import Big from 'big.js';
import { addMonths, addWeeks, addYears } from 'date-fns';
import { DataSource, EntityManager, In, Repository } from 'typeorm';
import { SubPlans, Subscription, SubscriptionHistory } from '../entities';
import { Period, PlanName, subscribe, SubscriptionStatus } from '../input';
import { DataInput, SubscriptionJobService } from './job.service';
import { Cron, CronExpression } from '@nestjs/schedule';
import { v4 as UUIDV4 } from 'uuid';

@Injectable()
export class SubscriptionService {
  private readonly logger = new Logger(SubscriptionService.name);

  constructor(
    @InjectRepository(Subscription)
    private readonly subscriptionRepository: Repository<Subscription>,
    @InjectRepository(SubscriptionHistory)
    private readonly historyRepository: Repository<SubscriptionHistory>,

    @Inject(forwardRef(() => SubscriptionJobService))
    private readonly schedulerService: SubscriptionJobService,
    private readonly paymentService: PaymentService,
    private dataSource: DataSource,
  ) {}

  async createSubscription(
    payload: subscribe,
    user: AuthUser,
  ): Promise<Subscription> {
    let firstTimer: boolean = false;
    let planName: PlanName = PlanName.free;

    const trailPaymentId = UUIDV4();
    const savedSubscription = await this.dataSource.manager.transaction(
      'REPEATABLE READ',
      async (manager) => {
        const plan = await manager.findOne(SubPlans, {
          where: { id: payload.planId },
        });

        if (!plan) {
          throw new ForbiddenException('Sorry!, Subscription plan not found');
        }

        planName = plan.name;
        const isFirstTime = await manager.find(SubscriptionHistory, {
          where: { user: { id: user.id } },
        });

        if (!isFirstTime.length) firstTimer = true;

        const price = firstTimer ? 0 : new Big(plan.price).toNumber();
        const startingDate = new Date();

        let expiringDate = addWeeks(startingDate, 1);
        if (!firstTimer) {
          if (plan.period === Period.month) {
            expiringDate = addMonths(startingDate, 1);
          } else if (plan.period === Period.year) {
            expiringDate = addYears(startingDate, 1);
          }
        }

        // 1. find if their is any active subscription
        //TODO add change the ending month
        const activeSubscription = await this.getActiveSubscription(user);
        if (activeSubscription) {
          throw new ForbiddenException('You have an active subscription');
        }

        // 2. create subscription history
        const history = manager.create(SubscriptionHistory, {
          user,
          plan,
          startingDate,
          expiringDate,
          price,
          status: SubscriptionStatus.pending,
        });

        // 3. save the subscription history
        const savedHistory = await manager.save(history);

        return savedHistory;
      },
    );

    // 4. charge the wallet or set trial payment ID
    let paymentId: string | undefined;

    if (!firstTimer) {
      if (planName === PlanName.free) {
        paymentId = trailPaymentId;
      } else {
        console.log('charging wallet');
        const { response } = await this.paymentService.internalDebitUser(
          {
            user: user,
            category: category.subscription,
            amount: savedSubscription.price,
          },
          true,
        );
        paymentId = response?.id;
      }
    } else {
      paymentId = trailPaymentId;
    }

    // 5. Update the subscription history with payment ID
    await this.historyRepository.update(
      { id: savedSubscription.id },
      { paymentId },
    );

    if (firstTimer || planName === PlanName.free) {
      this.updateSubscription({ paymentId: trailPaymentId });
    }

    return savedSubscription;
  }

  async getActiveSubscription(
    user: AuthUser,
    manager?: EntityManager,
  ): Promise<Subscription | null> {
    if (manager) {
      return manager.findOne(Subscription, {
        where: {
          user: { id: user.id },
          status: SubscriptionStatus.active,
        },
        relations: ['user', 'plan'],
      });
    }
    return this.subscriptionRepository.findOne({
      where: {
        user: { id: user.id },
        status: SubscriptionStatus.active,
      },
      relations: ['user', 'plan'],
    });
  }

  async systemUpdate(data: DataInput) {
    return this.dataSource.manager.transaction(async (manager) => {
      const history = await manager.findOne(SubscriptionHistory, {
        where: { id: data.subscriptionId },
        relations: ['user'],
      });

      if (!history) return;

      history.status = data.status;
      let reason: string = '';
      if (data.status === SubscriptionStatus.expired) {
        reason = 'Subscription expired';
      } else if (data.status === SubscriptionStatus.canceled) {
        reason = 'Subscription canceled';
      }
      await manager.save(SubscriptionHistory, history);

      const subscription = await manager.findOne(Subscription, {
        where: { user: { id: history.user.id } },
      });

      if (!subscription) return;

      subscription.status = data.status;

      const updateSubscription = await manager.save(Subscription, subscription);

      void this.repairMissingSchedules();
      return updateSubscription;
    });
  }

  // @Cron('*/1 * * * *')
  @Cron(CronExpression.EVERY_DAY_AT_MIDNIGHT)
  private async repairMissingSchedules(): Promise<void> {
    try {
      this.logger.log('Repairing missing schedules');
      // Find all active subscriptions without a scheduleId, that haven't expired yet
      const now = new Date();
      const orphanedSubs = await this.historyRepository.find({
        where: {
          status: SubscriptionStatus.active,
          scheduleId: In([undefined, null]),
          // expiringDate: MoreThan(now), // Get only not-yet-expired
        },
      });

      if (!orphanedSubs.length) return;

      for (const sub of orphanedSubs) {
        const delay = new Date(sub.expiringDate).getTime() - Date.now();
        const jobId = this.schedulerService.schedule(
          {
            subscriptionId: sub.id,
            status: SubscriptionStatus.expired,
          },
          delay,
        );

        // Update the scheduleId
        sub.scheduleId = jobId;
        await this.historyRepository.save(sub);
      }
    } catch (error) {
      this.logger.error(error);
    }
  }

  @OnEvent('execute.subscription', { async: true })
  private async updateSubscription(payload: { paymentId: string }) {
    try {
      return this.dataSource.manager.transaction(async (manager) => {
        const subscription = await manager.findOne(SubscriptionHistory, {
          where: {
            paymentId: payload.paymentId,
            status: SubscriptionStatus.pending,
          },
          relations: ['user', 'plan'],
        });

        if (!subscription) return;

        // Schedule expired date
        const delay = subscription.expiringDate.getTime() - Date.now();
        const schedule = this.schedulerService.schedule(
          {
            subscriptionId: subscription.id,
            status: SubscriptionStatus.expired,
          },
          delay,
        );

        subscription.status = SubscriptionStatus.active;
        subscription.scheduleId = schedule;
        await manager.save(subscription);

        const sub = await manager.findOne(Subscription, {
          where: { user: { id: subscription.id } },
        });

        if (!sub) {
          await manager.save(
            manager.create(Subscription, {
              user: subscription.user,
              plan: subscription.plan,
              status: SubscriptionStatus.active,
            }),
          );
        } else {
          sub.plan = subscription.plan;
          sub.status = SubscriptionStatus.active;
          await manager.save(sub);
        }
        return subscription;
      });
    } catch (error) {
      //TODO log the error
      this.logger.error(error);
    }
  }
}
