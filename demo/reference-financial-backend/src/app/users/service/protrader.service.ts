import { Document, DocumentResult } from '@app/common';
import {
  buildFindManyQuery,
  FindManyWrapper,
  FindOneWrapper,
} from '@app/helpers';
import { Trades } from '@app/trades/entities';
import { functionRetry, google } from '@app/utils';
import {
  BadRequestException,
  ForbiddenException,
  Injectable,
} from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository, TypeORMError } from 'typeorm';
import { inputScheme, outputSchema, PromptTemplate } from '../config';
import { Protrader, User } from '../entity';
import {
  createProTrader,
  findManyProTrader,
  findOneProTrader,
  Role,
} from '../interface';
import { nanoid } from 'nanoid';

@Injectable()
export class ProTraderService {
  constructor(
    @InjectRepository(Protrader)
    private readonly prorepo: Repository<Protrader>,

    @InjectRepository(User) private readonly userRepository: Repository<User>,
    @InjectRepository(Trades)
    private readonly tradeRepository: Repository<Trades>,
  ) {}

  async createProTrader(dto: createProTrader): Promise<Protrader> {
    try {
      const trader = await this.prorepo.findOneBy({ email: dto.email });
      if (trader) {
        throw new ForbiddenException(
          'Pro trader with this email already exists',
        );
      }
      const protrader = this.prorepo.create(dto);
      return this.prorepo.save(protrader);
    } catch (error) {
      if (error instanceof TypeORMError) {
        throw new ForbiddenException(error.message);
      }
      throw error;
    }
  }

  async findManyProTrader(
    query: findManyProTrader,
  ): Promise<DocumentResult<Protrader>> {
    try {
      const where = this.filter(query);
      const qb = this.prorepo.createQueryBuilder('protrader');
      buildFindManyQuery(
        qb,
        'protrader',
        where,
        query.search,
        ['name', 'email'],
        query.include,
        query.sort,
      );
      return FindManyWrapper(qb, query.page, query.limit);
    } catch (error) {
      if (error instanceof TypeORMError) {
        throw new ForbiddenException(error.message);
      }
      throw error;
    }
  }

  async findOneProtrader(
    query: findOneProTrader,
  ): Promise<Document<Protrader>> {
    try {
      const { include, sort, ...filters } = query;
      return FindOneWrapper<Protrader>(this.prorepo, {
        include,
        sort,
        filters,
      });
    } catch (error) {
      if (error instanceof TypeORMError) {
        throw new ForbiddenException(error.message);
      }
      throw error;
    }
  }

  async proTraderAiOverview(userId: string) {
    try {
      const user = await this.userRepository.findOneBy({
        id: userId,
        role: Role.pro,
      });

      if (!user) {
        throw new ForbiddenException('invalid credentials or user not found');
      }

      const trades = await this.tradeRepository.find({
        where: { creatorId: user.id },
      });

      return this.userAnalysis(user, trades);
    } catch (error) {
      if (error instanceof TypeORMError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  private filter(query: findManyProTrader) {
    const where: Record<string, any> = {};
    if (query.name) where['name'] = query.name;
    if (query.email) where['email'] = query.email;
    return where;
  }

  private async userAnalysis(user: User, trades: Trades[]) {
    const userAnalysis = google.defineFlow(
      {
        name: `user-prompt-${nanoid()}`,
        inputSchema: inputScheme,
        outputSchema: outputSchema,
      },
      async (input) => {
        try {
          return await functionRetry(async () => {
            const { output } = await PromptTemplate(input);
            return output!;
          });
        } catch (error) {
          console.log('AI User Analysis Error:', error);
          throw error;
        }
      },
    );

    // Transform trades to match the schema (convert Date fields to strings)
    const transformedTrades = trades.map((trade) => ({
      ...trade,
      startDate: trade.startDate.toISOString(),
      expiresAt: trade.expiresAt.toISOString(),
      createdAt: trade.createdAt.toISOString(),
      updatedAt: trade.updatedAt.toISOString(),
    }));

    return await userAnalysis({
      tradeData: transformedTrades,
      userData: {
        fullName: user.fullName,
        email: user.email,
        bio: user.bio,
        username: user.username,
        gender: user.gender,
      },
    });
  }
}
