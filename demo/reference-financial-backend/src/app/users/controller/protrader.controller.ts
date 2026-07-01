import { Abilities, Public } from '@app/decorators';
import {
  Body,
  Controller,
  Get,
  Param,
  Post,
  Query,
  VERSION_NEUTRAL,
} from '@nestjs/common';
import { ApiBearerAuth, ApiBody, ApiParam, ApiTags } from '@nestjs/swagger';
import {
  CreateProtrader,
  FindManyProTrader,
  FindOneProTrader,
  Overview,
} from '../dto';
import { ProTraderService } from '../service';

@Controller({ version: VERSION_NEUTRAL })
@ApiTags('Pro Traders')
@ApiBearerAuth()
export class ProtraderController {
  constructor(private readonly protraderService: ProTraderService) {}

  @Public()
  @Post('protrader')
  @ApiBody({ description: 'Create Pro Trader', type: CreateProtrader })
  createProtrader(@Body() dto: CreateProtrader) {
    return this.protraderService.createProTrader(dto);
  }

  @Get('protraders')
  @Abilities('MANAGE_PRO_TRADER_USER')
  findManyProtrader(@Query() query: FindManyProTrader) {
    return this.protraderService.findManyProTrader(query);
  }

  @Get('protrader')
  @Abilities('MANAGE_PRO_TRADER_USER')
  findOneProtrader(@Query() query: FindOneProTrader) {
    return this.protraderService.findOneProtrader(query);
  }

  @Get('protrade-ai-overview/:userId')
  @ApiParam({ name: 'userId', required: true, type: String })
  proTraderAiOverview(@Param() param: Overview) {
    return this.protraderService.proTraderAiOverview(param.userId);
  }
}
