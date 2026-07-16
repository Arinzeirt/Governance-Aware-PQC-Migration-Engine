import { AuthUser, ParamSearch } from '@app/common';
import { Abilities, SessionUser } from '@app/decorators';
import {
  Body,
  Controller,
  Delete,
  Get,
  Param,
  Post,
  Query,
  VERSION_NEUTRAL,
} from '@nestjs/common';
import {
  ApiBearerAuth,
  ApiBody,
  ApiOperation,
  ApiParam,
  ApiTags,
} from '@nestjs/swagger';
import {
  CreatePlan,
  CreateSubscription,
  FindManyHistory,
  FindOneHistory,
  UpdatePlan,
} from './input';
import { HistoryService, PlanService, SubscriptionService } from './service';

@Controller({ version: VERSION_NEUTRAL })
@ApiBearerAuth()
@ApiTags('Subscription')
export class SubscriptionController {
  constructor(
    private readonly subscriptionService: SubscriptionService,
    private readonly historyService: HistoryService,
    private readonly planService: PlanService,
  ) {}

  @Post('create-subscription')
  @ApiOperation({ summary: 'Create new subscription for a user' })
  @ApiBody({ type: CreateSubscription })
  createSubscription(
    @Body() dto: CreateSubscription,
    @SessionUser() user: AuthUser,
  ) {
    return this.subscriptionService.createSubscription(dto, user);
  }

  @Get('subscriptions')
  @ApiOperation({ summary: 'Find Many subscriptions' })
  findManySubscription(@Query() query: FindManyHistory) {
    return this.historyService.findMany(query);
  }

  @Get('subscription')
  @ApiOperation({ summary: 'Find One subscription history' })
  findOneSubscriptionHistory(@Query() query: FindOneHistory) {
    return this.historyService.findOne(query);
  }

  @Get('active-subscription')
  @ApiOperation({ summary: 'Get the active subscription of current user' })
  activeSubscription(@SessionUser() user: AuthUser) {
    return this.subscriptionService.getActiveSubscription(user);
  }

  @Post('create-plan')
  @Abilities('Plan.Create')
  @ApiOperation({ summary: 'Create new plan' })
  @ApiBody({ type: CreatePlan })
  createPlan(@Body() dto: CreatePlan) {
    return this.planService.createPlan(dto);
  }

  @Get('plans')
  @ApiOperation({ summary: 'Get all Plans' })
  findManyPlan() {
    return this.planService.findMany();
  }

  @Get('plan')
  @ApiParam({ name: 'id', type: String, format: 'uuid' })
  @ApiOperation({ summary: 'Get One plan' })
  findOnePlan(@Param() query: ParamSearch) {
    return this.planService.findOne(query.id);
  }

  @Post('update-plan')
  @Abilities('Plan.Update')
  @ApiParam({ name: 'id', type: String, format: 'uuid' })
  @ApiOperation({ summary: 'Update plan' })
  @ApiBody({ type: UpdatePlan })
  updatePlan(@Param() query: ParamSearch, @Body() dto: UpdatePlan) {
    return this.planService.update(query.id, dto);
  }

  @Delete('plan')
  @Abilities('Plan.Delete')
  @ApiParam({ name: 'id', type: String, format: 'uuid' })
  @ApiOperation({ summary: 'Delete plan' })
  deletePlan(@Param() query: ParamSearch) {
    return this.planService.delete(query.id);
  }
}
