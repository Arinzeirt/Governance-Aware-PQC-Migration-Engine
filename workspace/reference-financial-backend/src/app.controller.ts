import { Controller, Get, Redirect } from '@nestjs/common';
import { AppService } from './app.service';
import { Public } from './global/decorators';
import { ApiExcludeController } from '@nestjs/swagger';

@Controller()
@ApiExcludeController()
@Public()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get('hello')
  getHello(): string {
    return this.appService.getHello();
  }

  @Get('info')
  getInfo() {
    return this.appService.getInfo();
  }

  @Get()
  @Redirect('/docs', 302)
  redirectToDocs() {}
}
