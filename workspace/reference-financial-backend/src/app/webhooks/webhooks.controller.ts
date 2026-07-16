import { Public } from '@app/decorators';
import {
  Body,
  Controller,
  Get,
  Headers,
  HttpCode,
  HttpStatus,
  Post,
  Query,
  UseFilters,
} from '@nestjs/common';
import { ApiExcludeEndpoint, ApiOperation } from '@nestjs/swagger';
import { FindManyEvent, FindOneEvent } from './index';
import { WebhookExceptionFilter } from './webhook.exception.filter';
import { WebhooksService } from './webhooks.service';

@Public()
@Controller()
@UseFilters(WebhookExceptionFilter)
export class WebhooksController {
  constructor(private readonly webhookService: WebhooksService) {}

  @ApiExcludeEndpoint()
  @Post('webhooks/circle')
  @HttpCode(HttpStatus.OK)
  async handleCircleWebhook(
    @Body() payload: Buffer,
    @Headers('x-circle-key-id') keyId: string,
    @Headers('x-circle-signature') signature: string,
  ) {
    return this.webhookService.processCircleEvent(payload, keyId, signature);
  }

  @ApiExcludeEndpoint()
  @Post('webhooks/seerbit')
  @HttpCode(HttpStatus.OK)
  handleSerrbitWebhook(@Body() payload: Buffer) {
    return this.webhookService.processSeerBitEvent(payload);
  }

  @ApiExcludeEndpoint()
  @Post('webhooks/vt-pass')
  @HttpCode(HttpStatus.OK)
  handleVTPassWebhook(@Body() payload: Buffer) {
    return this.webhookService.processVTPassEvent(payload);
  }

  @Get('events')
  @ApiOperation({ summary: 'Get all the event logs' })
  async findManyEvent(@Query() query: FindManyEvent) {
    return this.webhookService.findManyEvent(query);
  }

  @Get('event')
  @ApiOperation({ summary: 'Get single event log' })
  async findOneEvent(@Query() query: FindOneEvent) {
    return this.webhookService.findOneEvent(query);
  }
}
