import { AuthUser } from '@app/common';
import {
  Abilities,
  ActiveSubscription,
  Public,
  SessionUser,
} from '@app/decorators';
import {
  Body,
  Controller,
  Delete,
  Get,
  Param,
  Patch,
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
  CreateTrade,
  FindManyTrade,
  FindOneTrade,
  Symbol,
  UpdateTrade,
} from '../input';
import { CreateTradeService, TradesService } from '../services';

@Controller({
  version: VERSION_NEUTRAL,
})
@ApiTags('TRADES')
@ApiBearerAuth()
export class TradesController {
  constructor(
    private readonly tradesService: TradesService,
    private readonly tradeService: CreateTradeService,
  ) {}

  @Post('trade')
  // @Abilities('TRADE_CREATE') //TODO remove comment
  @ApiOperation({ summary: 'Create new trade' })
  @ApiBody({ type: CreateTrade })
  create(@Body() createTrade: CreateTrade, @SessionUser() user: AuthUser) {
    return this.tradeService.createNewTrade(createTrade, user);
  }

  @Get('current-price')
  @ApiOperation({ summary: 'Get current price' })
  currentPrice(@Query() query: Symbol) {
    return this.tradeService.currentPrice(query.asset);
  }

  @Public()
  @Get('trader-status')
  TradeStatus(@Query('id') id: string) {
    return this.tradeService.checkTradeStatus(id);
  }

  @Get('trades')
  @ApiOperation({ summary: 'Get all the trades' })
  findAll(@Query() query: FindManyTrade) {
    return this.tradesService.findAll(query);
  }

  @Get('user-trades')
  @ApiOperation({ summary: 'Get all the trades' })
  findAllTradePostedByCurrentUser(
    @Query() query: FindManyTrade,
    @SessionUser() user: AuthUser,
  ) {
    return this.tradesService.findAll({ ...query, userId: [user.id] });
  }

  @Get('trade')
  // @ActiveSubscription()
  @ApiOperation({ summary: 'Get single trade' })
  findOne(@Query() query: FindOneTrade) {
    return this.tradesService.findOne(query);
  }

  @Get('trading-stats')
  @Abilities('TRADE_MANAGE')
  @ApiOperation({ summary: 'Get treading stats' })
  tradingStats(@SessionUser() user: AuthUser) {
    return this.tradesService.getTradingStats(user.id);
  }

  @Get('cancel-trade/:tradeId')
  @ApiOperation({ summary: 'Cancel on going trade' })
  @ApiParam({ type: String, name: 'tradeId', required: true })
  cancelTrade(
    @Param('tradeId') tradeId: string,
    @SessionUser() user: AuthUser,
  ) {
    return this.tradesService.cancelTrade(tradeId, user);
  }

  @Patch('trade/:tradeId')
  @Abilities('TRADE_UPDATE')
  @ApiOperation({ summary: 'Update un-start trade' })
  @ApiParam({ type: String, name: 'tradeId', required: true })
  @ApiBody({ type: UpdateTrade })
  update(
    @Param('tradeId') tradeId: string,
    @Body() updateTrade: UpdateTrade,
    @SessionUser() user: AuthUser,
  ) {
    return this.tradesService.update(tradeId, updateTrade, user);
  }

  @Delete('trade/:tradeId')
  @Abilities('TRADE_DELETE')
  @ApiOperation({ summary: 'Delete Trade' })
  @ApiParam({ type: String, name: 'tradeId', required: true })
  remove(@Param('tradeId') tradeId: string, @SessionUser() user: AuthUser) {
    return this.tradesService.remove(tradeId, user);
  }
}
