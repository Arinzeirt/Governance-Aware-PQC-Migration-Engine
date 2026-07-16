import { AuthUser, DocumentResult } from '@app/common';
import { buildFindManyQuery, FindManyWrapper } from '@app/helpers';
import { Role } from '@app/users/interface';
import { UsersService } from '@app/users/service';
import {
  ForbiddenException,
  Injectable,
  NotFoundException,
} from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { FollowTraders } from '../entities';
import { createFollower, getAllFollowing } from '../input';

@Injectable()
export class FollowingService {
  constructor(
    @InjectRepository(FollowTraders)
    private readonly followTrade: Repository<FollowTraders>,
    private readonly userService: UsersService,
  ) {}

  async followAndUnfollowTrader(
    data: createFollower,
    user: AuthUser,
  ): Promise<FollowTraders> {
    const trader = await this.userService.findOne({ id: data.followingId });
    if (!trader.data) {
      throw new NotFoundException('User with given id not found');
    }

    if (trader.data.role !== Role.pro) {
      throw new ForbiddenException('You can only follow pro traders');
    }

    const alreadyFollowing = await this.followTrade.findOne({
      where: {
        followerId: user.id,
        followingId: data.followingId,
      },
    });

    if (alreadyFollowing) {
      return this.followTrade.remove(alreadyFollowing);
    }
    return this.followTrade.save(
      this.followTrade.create({
        followerId: user.id,
        followingId: data.followingId,
      }),
    );
  }

  async getTraderFollowing(
    query: getAllFollowing,
  ): Promise<DocumentResult<FollowTraders>> {
    try {
      const where = this.filter(query);
      const qb = this.followTrade.createQueryBuilder('follow');
      buildFindManyQuery(
        qb,
        'follow',
        where,
        query.search,
        [],
        query.include,
        query.sort,
      );

      return FindManyWrapper(qb, query.page, query.limit);
    } catch (error) {
      throw error;
    }
  }

  private filter(query: getAllFollowing) {
    const where: Record<string, any> = {};
    if (query.followingId) where.followingId = query.followingId;
    if (query.followerId) where.followerId = query.followerId;

    return where;
  }
}
