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
  Airtime,
  Data,
  DataBundle,
  Electricity,
  VerifyElectricityName,
} from './input';
import { AirtimeService, DataService, ElectricityService } from './services';

@Controller({ version: VERSION_NEUTRAL })
@ApiBearerAuth()
@ApiTags('Utilities')
export class UtilitiesController {
  constructor(
    private readonly airtimeService: AirtimeService,
    private readonly dataService: DataService,
    private readonly electService: ElectricityService,
  ) {}

  @Post('airtime/purchase')
  @ApiBody({ type: Airtime })
  @ApiOperation({ summary: 'Purchase Airtime for users' })
  purchaseAirtime(@Body() payload: Airtime, @SessionUser() user: AuthUser) {
    return this.airtimeService.AirtimePurchase(payload, user);
  }

  @Post('data/Purchase')
  @ApiBody({ type: Data })
  @ApiOperation({ summary: 'Purchase Data bundle for users' })
  purchaseData(@Body() payload: Data, @SessionUser() user: AuthUser) {
    return this.dataService.dataPurchase(payload, user);
  }

  @Get('data/bundles')
  @ApiOperation({ summary: 'Get Available data bundles' })
  dataBundles(@Query() query: DataBundle) {
    return this.dataService.getAvailableData(query);
  }

  @Post('electricity/verify-name')
  @ApiOperation({ summary: 'Meter name verification' })
  @ApiBody({ type: VerifyElectricityName })
  nameVerification(@Body() payload: VerifyElectricityName) {
    return this.electService.verifyMeterNumber(payload);
  }

  @Get('electricity/companies')
  @ApiOperation({ summary: 'Get the list of all electricity companies' })
  electricityCompanies() {
    return this.electService.electricityCompanies();
  }

  @Post('electricity/purchase')
  @ApiOperation({ summary: 'Purchase Electricity for users' })
  @ApiBody({ type: Electricity })
  purchaseElectricity(
    @Body() payload: Electricity,
    @SessionUser() user: AuthUser,
  ) {
    return this.electService.ElectricityPurchase(payload, user);
  }
}
