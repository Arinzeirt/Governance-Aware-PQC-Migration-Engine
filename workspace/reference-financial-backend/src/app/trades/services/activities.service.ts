import { AuthUser, DocumentResult, findMany } from '@app/common';
import { buildFindManyQuery, FindManyWrapper } from '@app/helpers';
import { Role } from '@app/users/interface';
import { UsersService } from '@app/users/service';
import { forwardRef, Inject, Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { FollowTraders, TradeActivityFeeds, Trades } from '../entities';
import {
  allTraders,
  CopierBreakdown,
  copierInput,
  copierMap,
  createActivity,
  findManyActivity,
} from '../input';
import { TraderDefineService } from './trader-define.service';

@Injectable()
export class ActivityService {
  constructor(
    @InjectRepository(TradeActivityFeeds)
    private readonly activityRepo: Repository<TradeActivityFeeds>,
    @InjectRepository(FollowTraders)
    private readonly followTrade: Repository<FollowTraders>,
    @InjectRepository(Trades) private readonly tradeRepo: Repository<Trades>,
    @Inject(forwardRef(() => UsersService))
    private readonly userService: UsersService,
    private readonly tdService: TraderDefineService,
  ) {}

  create(create: createActivity): Promise<TradeActivityFeeds> {
    return this.activityRepo.save(this.activityRepo.create(create));
  }

  async allTraders(
    query: findMany,
    iuser: AuthUser,
  ): Promise<DocumentResult<allTraders>> {
    const proTraders = await this.userService.findMany({
      ...query,
      roleName: [Role.pro],
    });
    if (!proTraders) return proTraders;

    // Enrich each user in the data array
    const enrichedData = await Promise.all(
      proTraders.data.map(async (user) => {
        const totalFollowers = await this.followTrade.count({
          where: { followingId: user.id },
        });

        const isFollowing = await this.followTrade.findOne({
          where: {
            followerId: iuser.id,
            followingId: user.id,
          },
        });

        const roi = await this.tradeRepo.sum('tradeRoi', {
          creatorId: user.id,
        });

        const trades = await this.tradeRepo.find({
          where: { creatorId: user.id },
        });

        let totalWeightedRisk = 0;
        let totalPositionSize = 0;

        trades.forEach((trade) => {
          if (
            trade.stopLoss &&
            trade.entryPrice &&
            trade.positionSize?.amount
          ) {
            const risk =
              (Math.abs(trade.entryPrice - trade.stopLoss) *
                trade.positionSize.amount) /
              trade.entryPrice;
            totalWeightedRisk += risk * trade.positionSize.amount;
            totalPositionSize += trade.positionSize.amount;
          }
        });

        const riskScore =
          totalPositionSize > 0 ? totalWeightedRisk / totalPositionSize : 0;
        const data = {
          totalFollowers,
          roi,
          riskScore,
          isFollowing: !!isFollowing,
        };
        return { ...user, ...data };
      }),
    );

    // Return the full response, replacing data with enrichedData
    return {
      ...proTraders,
      data: enrichedData,
    };
  }

  async findMany(
    query: findManyActivity,
  ): Promise<DocumentResult<TradeActivityFeeds>> {
    const qb = this.activityRepo.createQueryBuilder('activity');
    buildFindManyQuery(
      qb,
      'activity',
      this.tdService.filter(query),
      query.search,
      ['title', 'message'],
      query.include,
      query.sort,
    );

    return FindManyWrapper(qb, query.page, query.limit);
  }
}
