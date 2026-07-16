import { JobQueueService } from '@app/services';
import {
  BadRequestException,
  Inject,
  Injectable,
  OnModuleDestroy,
  OnModuleInit,
  forwardRef,
} from '@nestjs/common';
import { defineWorker } from 'plainjob';
import {
  copyTraders,
  placeTrade,
  placeTradeJob,
  refundTradePayment,
  refundTradePaymentJob,
  scheduleTrade,
  traders,
} from '../input';
import { ExecuteTradeService } from './execute-trade.service';
import { TradesService } from './trades.service';
import { TradeDefineService } from './define.service';

const trading = 'trades';
const rt = 'reprocessTrading';
const refund = 'refundTradePayment';
const follower = 'sendNotificationToFollowers';

@Injectable()
export class TradeJobWorker implements OnModuleInit, OnModuleDestroy {
  private readonly jobQueueService = new JobQueueService();
  constructor(
    @Inject(forwardRef(() => TradesService))
    private readonly tradesService: TradesService,

    @Inject(forwardRef(() => ExecuteTradeService))
    private readonly executeTradeService: ExecuteTradeService,

    @Inject(forwardRef(() => TradeDefineService))
    private readonly tradeDService: TradeDefineService,
  ) {}

  onModuleInit() {
    this.startWorkers().catch((err) => {
      console.log('Trade Notification sending not working', err);
    });
  }

  onModuleDestroy() {
    this.stopWorkers().catch(() => {
      process.exit(1);
    });
  }

  scheduleTrade(data: scheduleTrade, delay: number) {
    const JobId = this.jobQueueService.jobQueue.add(trading, data, { delay });
    return JobId.id;
  }

  reprocessTrading(data: placeTrade, delay: number) {
    return this.jobQueueService.jobQueue.add(rt, data, { delay });
  }

  sendNotificationToFollowers(data: copyTraders) {
    const { id } = this.jobQueueService.jobQueue.add(follower, data);
    return id;
  }

  refundTradePayment(data: refundTradePayment, delay: number) {
    return this.jobQueueService.jobQueue.add(refund, data, { delay });
  }

  closeJob(jobId: number) {
    return this.jobQueueService.jobQueue.markJobAsDone(jobId);
  }

  private async startWorkers() {
    await Promise.all([
      this.sendNotification.start(),
      this.tradePayment.start(),
      this.refundTPWorker.start(),
    ]);
  }

  private async stopWorkers() {
    await Promise.all([
      this.sendNotification.stop(),
      this.tradePayment.stop(),
      this.refundTPWorker.stop(),
    ]);
  }

  private async handleSendNotification(
    data: string | copyTraders,
  ): Promise<void> {
    let details: copyTraders;
    try {
      details = typeof data === 'string' ? await JSON.parse(data) : data;

      await this.tradesService.sendNotificationJob(details);
    } catch (error) {
      console.error('Error processing Trade job:', error);
      throw error;
    }
  }

  private readonly sendNotification = defineWorker(
    follower,
    async (job: traders) => {
      await this.handleSendNotification(job.data);
    },
    {
      queue: this.jobQueueService.jobQueue,
      onCompleted: (job) => console.log(`✅ Job ${job.id} completed`),
      onFailed: (job, error) =>
        console.error(`❌ Job ${job.id} failed: ${error}`),
      pollIntervall: 5000,
      logger: {
        info() {},
        error(message) {
          console.error(message);
        },
        warn() {},
        debug() {},
      },
    },
  );

  private readonly tradePayment = defineWorker(
    rt,
    async (job: placeTradeJob) => {
      await this.handleReprocessTrading(job.data);
    },
    {
      queue: this.jobQueueService.jobQueue,
      onCompleted: (job) => console.log(`Job ${job.id} completed`),
      onFailed: (job, error) => console.error(`Job ${job.id} failed: ${error}`),
      pollIntervall: 5000,
      logger: {
        info() {},
        error(message) {
          console.error(message);
        },
        warn() {},
        debug() {},
      },
    },
  );

  private readonly refundTPWorker = defineWorker(
    refund,
    async (job: refundTradePaymentJob) => {
      await this.handleRefundTP(job.data);
    },
    {
      queue: this.jobQueueService.jobQueue,
      onCompleted: (job) => console.log(`Job ${job.id} completed`),
      onFailed: (job, error) => console.error(`Job ${job.id} failed: ${error}`),
      pollIntervall: 5000,
      logger: {
        info() {},
        error(message) {
          console.error(message);
        },
        warn() {},
        debug() {},
      },
    },
  );

  private async handleReprocessTrading(data: string | placeTrade) {
    try {
      const payload =
        typeof data === 'string' ? (JSON.parse(data) as placeTrade) : data;
      await this.executeTradeService.handleTradeExecution(payload);
      return;
    } catch (error) {
      if (error instanceof Error) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  private async handleRefundTP(data: string | refundTradePayment) {
    try {
      const payload =
        typeof data === 'string'
          ? (JSON.parse(data) as refundTradePayment)
          : data;
      await this.tradeDService.handleTradeRefund(
        payload.userId,
        payload.amount,
      );
      return;
    } catch (error) {
      if (error instanceof Error) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }
}
