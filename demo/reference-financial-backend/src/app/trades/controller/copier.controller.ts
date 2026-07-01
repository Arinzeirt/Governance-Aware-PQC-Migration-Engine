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
import {
  CopierBreakdown,
  CopierProfilePerformance,
  CopyTrading,
} from '../input';
import { CopierService, CopierTradeService } from '../services';

@Controller({ version: VERSION_NEUTRAL })
@ApiTags('COPIER TRADERS')
@ApiBearerAuth()
export class CopierController {
  constructor(
    private readonly copierService: CopierService,
    private readonly copierTrade: CopierTradeService,
  ) {}

  @Post('copy-trade')
  @ApiOperation({ summary: 'Copy trades' })
  @ApiBody({ type: CopyTrading })
  copyTrade(@Body() body: CopyTrading, @SessionUser() user: AuthUser) {
    return this.copierTrade.CopyTrade(body, user);
  }

  @Get('user-dashboard-stats')
  @ApiOperation({ summary: 'Get trade dashboard stats' })
  dashboardStats(@SessionUser() user: AuthUser) {
    return this.copierService.getUserAssetDashboard(user);
  }

  @Get('performance-breakdown')
  @ApiOperation({ summary: 'Get user performance breakdown' })
  performanceBreakdown(
    @Query() query: CopierProfilePerformance,
    @SessionUser() user: AuthUser,
  ) {
    return this.copierService.performanceBreakdown(query.period, user);
  }

  @Get('copier-breakdown')
  @ApiOperation({ summary: 'Get copier breakdown' })
  copierBreakdown(@Query() query: CopierBreakdown) {
    return this.copierService.copierBreakdown(query);
  }
}
