import { BadRequestException, Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import {
  endOfMonth,
  endOfWeek,
  startOfMonth,
  startOfWeek,
  subWeeks,
} from 'date-fns';
import { Between, In, Repository, TypeORMError } from 'typeorm';
import { User, UserActivity } from '../entity';
import {
  dashboardFilter,
  dashChartResponse,
  dashStatsResponse,
  Role,
  Row,
} from '../interface';

@Injectable()
export class AdminService {
  constructor(
    @InjectRepository(User) private readonly repo: Repository<User>,
    @InjectRepository(UserActivity)
    private readonly userActivityRepository: Repository<UserActivity>,
  ) {}

  async dashboardStats(): Promise<dashStatsResponse> {
    try {
      const weekStart = startOfWeek(new Date(), { weekStartsOn: 1 });
      const weekEnd = endOfWeek(new Date(), { weekStartsOn: 1 });

      const startOfLastWeek = startOfWeek(subWeeks(new Date(), 1), {
        weekStartsOn: 1,
      });
      const endOfLastWeek = endOfWeek(subWeeks(new Date(), 1), {
        weekStartsOn: 1,
      });

      const [
        totalUsers,
        totalActiveUser,
        totalCopiers,
        totalProTraders,
        lastWeekCopies,
        thisWeekCopies,
        lastWeekProTrades,
        thisWeekProTrades,
        activeThisWeek,
        activeLastWeek,
      ] = await Promise.all([
        this.repo.count(),
        this.activeUsers(),
        this.repo.count({ where: { role: Role.follower } }),
        this.repo.count({ where: { role: Role.pro } }),
        this.repo.count({
          where: {
            role: Role.follower,
            createdAt: Between(startOfLastWeek, endOfLastWeek),
          },
        }),
        this.repo.count({
          where: {
            role: Role.follower,
            createdAt: Between(weekStart, weekEnd),
          },
        }),
        this.repo.count({
          where: {
            role: Role.pro,
            createdAt: Between(startOfLastWeek, endOfLastWeek),
          },
        }),
        this.repo.count({
          where: { role: Role.pro, createdAt: Between(weekStart, weekEnd) },
        }),
        this.getWeeklyActiveUsers(weekStart, weekEnd),
        this.getWeeklyActiveUsers(startOfLastWeek, endOfLastWeek),
      ]);

      const lastWeekCopyChange = this.calculatePercentageChange(
        lastWeekCopies,
        thisWeekCopies,
      );

      const lastWeekProTradeChange = this.calculatePercentageChange(
        lastWeekProTrades,
        thisWeekProTrades,
      );

      const activeChange = this.calculatePercentageChange(
        activeLastWeek,
        activeThisWeek,
      );

      const isIncrease = (change: number) => change > 0;
      return {
        totalUsers,
        activeUser: {
          total: totalActiveUser,
          change: activeChange,
          increase: isIncrease(activeChange),
        },
        copiers: {
          total: totalCopiers,
          change: lastWeekCopyChange,
          increase: isIncrease(lastWeekCopyChange),
        },
        proTraders: {
          total: totalProTraders,
          change: lastWeekProTradeChange,
          increase: isIncrease(lastWeekProTradeChange),
        },
      };
    } catch (error) {
      if (error instanceof TypeORMError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  async dashboardChart(filter: dashboardFilter): Promise<dashChartResponse[]> {
    try {
      const allUsers = await this.repo.find({
        where: { role: In([Role.pro, Role.follower]) },
      });

      const current = new Date();
      const weekStart = startOfWeek(current, { weekStartsOn: 1 });
      const weekEnd = endOfWeek(current, { weekStartsOn: 1 });
      const monthStart = startOfMonth(current);
      const monthEnd = endOfMonth(current);

      const qb = this.userActivityRepository
        .createQueryBuilder('activity')
        .select([]) // ← prevents auto-select of activity.id
        .leftJoin('activity.user', 'user') // no need for select here
        .addSelect('COUNT(DISTINCT activity.userId)', 'active')
        .addSelect(
          `COALESCE(
        JSON_AGG(DISTINCT JSONB_BUILD_OBJECT('id', "user"."id", 'role', "user"."role")),
        '[]'::json
    )`,
          'users',
        );

      /** APPLY FILTERS -------------------------------------------------------- */
      if (filter.range === 'this year') {
        qb.andWhere('EXTRACT(YEAR FROM activity.date) = :year', {
          year: current.getFullYear(),
        });
      }

      if (filter.range === 'this month') {
        qb.andWhere('activity.date BETWEEN :monthStart AND :monthEnd', {
          monthStart,
          monthEnd,
        });
      }

      if (filter.range === 'this week') {
        qb.andWhere('activity.date BETWEEN :weekStart AND :weekEnd', {
          weekStart,
          weekEnd,
        });
      }

      if (filter.from && filter.to) {
        qb.andWhere('activity.date BETWEEN :from AND :to', {
          from: filter.from,
          to: filter.to,
        });
      }

      /** DYNAMIC BUCKETS + GROUPING ------------------------------------------ */
      let buckets: string[] = [];
      let groupField = '';
      // let bucketLabelSelect = '';

      if (filter.range === 'this year') {
        buckets = [
          'Jan',
          'Feb',
          'Mar',
          'Apr',
          'May',
          'Jun',
          'Jul',
          'Aug',
          'Sep',
          'Oct',
          'Nov',
          'Dec',
        ];
        groupField = 'EXTRACT(MONTH FROM activity.date)';

        qb.addSelect("TO_CHAR(activity.date, 'Mon')", 'label');
        qb.addSelect(groupField, 'bucket');
      }

      if (filter.range === 'this month') {
        const days = endOfMonth(current).getDate();
        buckets = Array.from({ length: days }, (_, i) => (i + 1).toString());
        groupField = 'EXTRACT(DAY FROM activity.date)';

        qb.addSelect(groupField, 'label');
        qb.addSelect(groupField, 'bucket');
      }

      if (filter.range === 'this week') {
        buckets = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
        groupField = 'EXTRACT(DOW FROM activity.date)'; // Sunday = 0

        qb.addSelect("TO_CHAR(activity.date, 'Dy')", 'label');
        qb.addSelect(groupField, 'bucket');
      }

      qb.groupBy('label').addGroupBy('bucket').orderBy('bucket', 'ASC');
      const data = await qb.getRawMany();

      const activityMap = new Map<number, Row>();

      for (const row of data) {
        let bucketNum = Number(row.bucket);

        if (filter.range === 'this week') {
          if (bucketNum === 0) bucketNum = 7;
        }

        // eslint-disable-next-line @typescript-eslint/no-unsafe-argument
        activityMap.set(bucketNum, row);
      }

      return buckets.map((label, index) => {
        const bucketNumber = index + 1;

        const row = activityMap.get(bucketNumber);

        const activeUsers = row && Array.isArray(row.users) ? row.users : [];
        const activeSet = new Set(activeUsers.map((u) => u.id));

        const activeRoles = this.reducer(activeUsers);

        const inactiveUsers = allUsers.filter((u) => !activeSet.has(u.id));
        const inactiveRoles = this.reducer(inactiveUsers);

        const usersRole = this.reducer(allUsers);

        return {
          label,
          users: { total: allUsers.length, ...usersRole },
          active: { total: activeUsers.length, ...activeRoles },
          inactive: { total: inactiveUsers.length, ...inactiveRoles },
        };
      });
    } catch (error) {
      if (error instanceof TypeORMError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  private calculatePercentageChange = (
    lastWeekCount: number,
    thisWeekCount: number,
  ) => {
    if (lastWeekCount === 0) return thisWeekCount === 0 ? 0 : 100;
    return ((thisWeekCount - lastWeekCount) / lastWeekCount) * 100;
  };

  private async getWeeklyActiveUsers(
    weekStart: Date,
    weekEnd: Date,
  ): Promise<number> {
    const result = await this.userActivityRepository
      .createQueryBuilder('activity')
      .select('COUNT(DISTINCT activity.userId)', 'count')
      .where('activity.date BETWEEN :start AND :end', {
        start: weekStart,
        end: weekEnd,
      })
      .getRawOne();

    return Number(result.count);
  }

  private async activeUsers(): Promise<number> {
    const result = await this.userActivityRepository
      .createQueryBuilder('activity')
      .select('COUNT(DISTINCT activity.userId)', 'count')
      .getRawOne();

    return Number(result.count);
  }

  private reducer(filter: { id: string; role: Role }[]) {
    return filter.reduce(
      (acc, user) => {
        if (user.role === Role.pro) acc.Protraders += 1;
        if (user.role === Role.follower) acc.followers += 1;
        return acc;
      },
      { Protraders: 0, followers: 0 },
    );
  }
}
