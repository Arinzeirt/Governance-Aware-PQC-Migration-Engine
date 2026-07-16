import { AuthUser, ParamSearch } from '@app/common';
import { SessionUser } from '@app/decorators';
import { Controller, Get, Param, Query, VERSION_NEUTRAL } from '@nestjs/common';
import {
  ApiBearerAuth,
  ApiOperation,
  ApiParam,
  ApiTags,
} from '@nestjs/swagger';
import { ProfilePerformance } from '../input';
import { ProTradePerformance } from '../services';

@Controller({ version: VERSION_NEUTRAL })
@ApiTags('PRO-TRADERS')
@ApiBearerAuth()
export class TraderController {
  constructor(private readonly performance: ProTradePerformance) {}

  @Get('trader-profile-stats/:id') //TODO trader profile info 8338f189-1423-4ebf-8ae4-a0243a378e11
  @ApiOperation({ summary: 'Get trader profile stats add protrader Id' })
  @ApiParam({ required: true, name: 'id', type: String, format: 'uuid' })
  getTraderStats(@SessionUser() user: AuthUser, @Param() param: ParamSearch) {
    return this.performance.tradeProfileStats(param.id, user);
  }

  @Get('trader-profile-performance')
  @ApiOperation({ summary: 'Get trader performances' })
  profilePerformance(@Query() query: ProfilePerformance) {
    return this.performance.profitPerformance(query.period, query.userId);
  }

  @Get('trader-graph')
  @ApiOperation({ summary: 'Get the trader graph' })
  traderGraph(@Query() query: ProfilePerformance) {
    return this.performance.graph(query.period, query.userId);
  }

  @Get('asset-performance/:userId')
  @ApiOperation({ summary: 'Get the asset trade details' })
  @ApiParam({ required: true, name: 'userId', type: String })
  assetTrade(@Param('userId') param: string) {
    return this.performance.getAssetPerformance(param);
  }

  @Get('copier-performance')
  @ApiOperation({ summary: 'Get the copier performance' })
  CopiersPerformance(@Query() query: ProfilePerformance) {
    return this.performance.copierPerformance(query.period, query.userId);
  }
}
