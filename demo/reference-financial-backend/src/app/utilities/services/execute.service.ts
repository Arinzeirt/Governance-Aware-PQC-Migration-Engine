import { Transaction } from '@app/wallets/entities';
import { Injectable, Logger } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { DefineService } from './define.service';
import { OnEvent } from '@nestjs/event-emitter';

@Injectable()
export class ExecuteService {
  private readonly logger = new Logger(ExecuteService.name);
  constructor(
    @InjectRepository(Transaction)
    private readonly transRepository: Repository<Transaction>,

    private readonly ds: DefineService,
  ) {}

  @OnEvent('execute.utility', { async: true })
  async execute(payload: { paymentId: string }): Promise<void> {
    const transaction = await this.transRepository.findOne({
      where: { externalRef: payload.paymentId },
      relations: ['bills', 'user'],
    });

    if (!transaction) {
      this.logger.error(
        `Transaction not found for paymentId: ${payload.paymentId}`,
      );
      return;
    }

    const { bills, user } = transaction;
    if (!bills) {
      this.logger.error(`Bills not found for transaction: ${transaction.id}`);
      return;
    }

    const response = await this.ds.handleUtilityPayment(bills.payload);
    await this.ds.handleUtilityPurchase(response, transaction, user);
    return;
  }
}
