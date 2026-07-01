import { AuthUser } from '@app/common';
import { Injectable, OnModuleDestroy, OnModuleInit } from '@nestjs/common';
import { JobQueueService } from '@app/services';
import { defineWorker, Job as plainJob } from 'plainjob';
import { SeerBitService, USDCService } from '@app/wallets/service';

const JobName = 'create-crypto-account';
const Job_Name = 'create-virtual-account';

type Job = plainJob & {
  data: AuthUser;
};

@Injectable()
export class UserScheduleService implements OnModuleInit, OnModuleDestroy {
  private readonly jobQueueService = new JobQueueService();
  constructor(
    private readonly usdcService: USDCService,
    private readonly seerBitService: SeerBitService,
  ) {}

  onModuleInit() {
    this.accountWorkerStart().catch((err) => {
      console.error('Blog worker not start:', err);
      process.exit(1);
    });
  }

  onModuleDestroy() {
    this.accountWorkerStop().catch(() => {
      process.exit(1);
    });
  }

  createCryptoAccount(data: AuthUser) {
    this.jobQueueService.jobQueue.add(JobName, data);
  }

  createVirtualAccount(data: AuthUser, delay: number) {
    this.jobQueueService.jobQueue.add(Job_Name, data, {
      delay,
    });
  }

  private readonly worker = defineWorker(
    JobName,
    async (job: Job) => {
      await this.usdcService.createWalletForUser(job.data);
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

  private readonly va_worker = defineWorker(
    Job_Name,
    async (job: Job) => {
      await this.seerBitService.createVirtualAccount(job.data);
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

  private async accountWorkerStart() {
    await Promise.all([this.va_worker.start(), this.worker.start()]);
  }

  private async accountWorkerStop() {
    await Promise.all([this.va_worker.stop(), this.worker.stop()]);
  }
}
