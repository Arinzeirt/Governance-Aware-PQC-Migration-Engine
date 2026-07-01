import { AuthUser } from '@app/common';
import { SessionUser } from '@app/decorators';
import {
  Body,
  Controller,
  Get,
  Post,
  Query,
  VERSION_NEUTRAL,
} from '@nestjs/common';
import { ApiBearerAuth, ApiBody, ApiOperation, ApiTags } from '@nestjs/swagger';
import { CreateFollower, GetAllFollowing } from '../input';
import { FollowingService } from '../services';

@Controller({ version: VERSION_NEUTRAL })
@ApiTags('FOLLOWING')
@ApiBearerAuth()
export class FollowController {
  constructor(private readonly follow: FollowingService) {}

  @Post('follow-trader')
  @ApiOperation({
    summary:
      'Follow a trader first click follow the pro trader the second click remove the follow',
  })
  @ApiBody({ type: CreateFollower })
  followTrader(@Body() body: CreateFollower, @SessionUser() user: AuthUser) {
    return this.follow.followAndUnfollowTrader(body, user);
  }

  @Get('following-traders')
  @ApiOperation({ summary: 'Get following traders' })
  getFollowing(@Query() query: GetAllFollowing, @SessionUser() user: AuthUser) {
    return this.follow.getTraderFollowing({ ...query, followerId: [user.id] });
  }

  @Get('followers')
  @ApiOperation({ summary: 'Get followers' })
  getFollowers(@Query() query: GetAllFollowing, @SessionUser() user: AuthUser) {
    return this.follow.getTraderFollowing({ ...query, followingId: [user.id] });
  }
}
