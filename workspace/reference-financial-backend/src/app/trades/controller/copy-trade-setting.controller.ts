import { AuthUser } from '@app/common';
import { SessionUser } from '@app/decorators';
import { Body, Controller, Post, VERSION_NEUTRAL } from '@nestjs/common';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
import { CopySettings } from '../input';
import { CopyTradeSettingsService } from '../services';

@Controller({ version: VERSION_NEUTRAL })
@ApiTags('Copy Trade Settings')
@ApiBearerAuth()
export class CopyTradeSettingsController {
  constructor(private readonly copySettings: CopyTradeSettingsService) {}

  @Post('copy-trade-setting')
  async createCopySetting(
    @Body() copySetting: CopySettings,
    @SessionUser() user: AuthUser,
  ) {
    return await this.copySettings.createCopySetting(copySetting, user);
  }
}
