import { FindMany } from '@app/common';
import { Controller, Get, Query, VERSION_NEUTRAL } from '@nestjs/common';
import { ApiBearerAuth, ApiOperation, ApiTags } from '@nestjs/swagger';
import { FindManyActivity } from '../input';
import { ActivityService } from '../services';
import { AuthUser } from '@app/common';
import { SessionUser } from '@app/decorators';

@Controller({ version: VERSION_NEUTRAL })
@ApiTags('ACTIVITIES')
@ApiBearerAuth()
export class ActivitiesController {
  constructor(private readonly activity: ActivityService) {}

  @Get('activities')
  @ApiOperation({ summary: 'Find users Activities' })
  ActivityFeeds(@Query() query: FindManyActivity) {
    return this.activity.findMany(query);
  }

  @Get('traders')
  @ApiOperation({ summary: 'Find all traders' })
  findAllTraders(@Query() query: FindMany, @SessionUser() user: AuthUser) {
    return this.activity.allTraders(query, user);
  }
}
