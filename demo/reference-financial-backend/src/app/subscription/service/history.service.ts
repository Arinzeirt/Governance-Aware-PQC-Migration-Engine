import { Document, DocumentResult } from '@app/common';
import {
  buildFindManyQuery,
  FindManyWrapper,
  FindOneWrapper,
} from '@app/helpers';
import { Injectable, InternalServerErrorException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository, TypeORMError } from 'typeorm';
import { SubscriptionHistory } from '../entities';
import { findManySubHistory, findOneSubHistory } from '../input';

@Injectable()
export class HistoryService {
  constructor(
    @InjectRepository(SubscriptionHistory)
    private readonly historyRepository: Repository<SubscriptionHistory>,
  ) {}

  async findMany(
    query: findManySubHistory,
  ): Promise<DocumentResult<SubscriptionHistory>> {
    try {
      const { page, sort, limit, include, search, ...filter } = query;
      const where = this.filterHistory(filter);
      const qb = this.historyRepository.createQueryBuilder('history');

      buildFindManyQuery(qb, 'history', where, search, [], include, sort);
      return FindManyWrapper(qb, page, limit);
    } catch (error) {
      if (error instanceof TypeORMError) {
        throw new InternalServerErrorException();
      }
      throw error;
    }
  }

  async findOne(
    query: findOneSubHistory,
  ): Promise<Document<SubscriptionHistory>> {
    try {
      const { include, sort, ...filters } = query;
      const { userId, planId, ...rest } = filters;
      if (userId) rest.user = { id: userId };
      if (planId) rest.plan = { id: planId };
      return FindOneWrapper<SubscriptionHistory>(this.historyRepository, {
        include,
        sort,
        filters,
      });
    } catch (error) {
      if (error instanceof TypeORMError) {
        throw new InternalServerErrorException();
      }
      throw error;
    }
  }

  private filterHistory(query: findManySubHistory): Record<string, any> {
    const where: Record<string, any> = {};

    if (query.user) where['user'] = { id: query.user };
    if (query.plan) where['plan'] = { id: query.plan };
    if (query.paymentId) where['paymentId'] = query.paymentId;
    if (query.startingDate) where['startingDate'] = query.startingDate;
    if (query.expiringDate) where['expiringDate'] = query.expiringDate;

    return where;
  }
}
