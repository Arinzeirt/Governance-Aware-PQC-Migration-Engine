import {
  BadRequestException,
  Injectable,
  OnModuleDestroy,
  OnModuleInit,
} from '@nestjs/common';
import { JobQueueService } from '@app/services';
import { defineWorker, Job as plainJob } from 'plainjob';
import { AuthUser } from '@app/common';
import { Between, Repository, TypeORMError } from 'typeorm';
import { InjectRepository } from '@nestjs/typeorm';
import { Transaction, Wallets } from '../entities';
import { transactionStatus, walletSymbol } from '../input';
import Big from 'big.js';
import { endOfDay, startOfDay } from 'date-fns';

interface Funding {
  externalRef?: string;
  user: AuthUser;
  currency: walletSymbol;
  amount: string;
}

type Job = plainJob & {
  data: Funding;
};

const JobName = 'fund-user-convert';

@Injectable()
export class WalletScheduler implements OnModuleInit, OnModuleDestroy {
  private readonly jobQueueService = new JobQueueService();
  constructor(
    @InjectRepository(Transaction)
    private readonly transRepo: Repository<Transaction>,
    @InjectRepository(Wallets) private readonly walletRepo: Repository<Wallets>,
  ) {}

  onModuleInit() {
    this.fundingWorkerStart().catch((err) => {
      console.error('funding User not start:', err);
      process.exit(1);
    });
  }

  onModuleDestroy() {
    this.fundingWorkerStop().catch(() => {
      process.exit(1);
    });
  }

  fundingUserAccount(data: Funding, delay: number) {
    this.jobQueueService.jobQueue.add(JobName, data, { delay });
  }

  private readonly worker = defineWorker(
    JobName,
    async (job: Job) => {
      await this.fundingUser(job.data);
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

  private async fundingWorkerStart() {
    await this.worker.start();
  }

  private async fundingWorkerStop() {
    await this.worker.stop();
    this.jobQueueService.jobQueue.close();
  }

  private async fundingUser(data: string | Funding) {
    try {
      const funding: Funding =
        typeof data === 'string' ? (JSON.parse(data) as Funding) : data;
      const today = new Date();
      const startToday = startOfDay(today);
      const endToday = endOfDay(today);

      if (!funding.externalRef) return;

      const transaction = await this.transRepo.findOneBy({
        externalRef: funding.externalRef,
        createdAt: Between(startToday, endToday),
      });

      if (!transaction) return;
      console.log(transaction.status);
      if (transaction.status !== transactionStatus.complete) {
        const delay = new Date(new Date().setTime(60_000)).getTime();
        return this.fundingUserAccount(funding, delay);
      }

      const fund = await this.walletRepo.findOneBy({
        user: { id: funding.user.id },
        currency: funding.currency,
      });
      if (!fund) {
        return this.walletRepo.save(
          this.walletRepo.create({
            user: { id: funding.user.id },
            currency: funding.currency,
            balance: Big(funding.amount).toNumber(),
          }),
        );
      }
      transaction.currentBal = Big(transaction.currentBal)
        .add(Big(funding.amount))
        .toNumber();
      await this.transRepo.save(transaction);

      fund.balance = Big(fund.balance).add(Big(funding.amount)).toNumber();
      return this.walletRepo.save(fund);
    } catch (error) {
      if (error instanceof TypeORMError) {
        throw new BadRequestException(error);
      }
      throw error;
    }
  }
}
