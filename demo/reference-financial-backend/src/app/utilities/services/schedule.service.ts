import {
  BadRequestException,
  forwardRef,
  Inject,
  Injectable,
  OnModuleDestroy,
  OnModuleInit,
} from '@nestjs/common';
import { DefineService } from './define.service';
import { defineWorker, Job as plainJob } from 'plainjob';
import { JobQueueService } from '@app/services';
import { AxiosError } from 'axios';
import { requery } from '../input';

type Job = plainJob & {
  data: requery;
};

const JobName = 'utility-purchase';

@Injectable()
export class ScheduleService implements OnModuleInit, OnModuleDestroy {
  private readonly jobQueueService = new JobQueueService();
  constructor(
    @Inject(forwardRef(() => DefineService))
    private readonly defineService: DefineService,
  ) {}

  onModuleInit() {
    this.requeryWorkerStart().catch((err) => {
      console.error('Requery worker not start:', err);
      process.exit(1);
    });
  }

  onModuleDestroy() {
    this.requeryWorkerStop().catch(() => {
      process.exit(1);
    });
  }

  scheduleRequery(data: requery, delay: number) {
    const { id } = this.jobQueueService.jobQueue.add(JobName, data, { delay });
    return id;
  }

  private async requeryWorkerStart() {
    await this.worker.start();
  }

  private async requeryWorkerStop() {
    await this.worker.stop();
    this.jobQueueService.jobQueue.close();
  }

  private readonly worker = defineWorker(
    JobName,
    async (job: Job) => {
      await this.handlePaymentRequery(job.data);
    },
    {
      queue: this.jobQueueService.jobQueue,
      onCompleted: () => {},
      onFailed: () => {},
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

  private async handlePaymentRequery(data: string | requery) {
    try {
      const payload =
        typeof data === 'string' ? (JSON.parse(data) as requery) : data;
      return await this.defineService.requeryTransaction(payload);
    } catch (error) {
      if (error instanceof AxiosError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }
}
