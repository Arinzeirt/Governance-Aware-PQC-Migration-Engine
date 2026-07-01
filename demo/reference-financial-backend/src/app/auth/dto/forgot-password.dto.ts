import { ApiProperty } from '@nestjs/swagger';
import { IsEmail } from 'class-validator';

export class ForgotPasswordDto {
  @ApiProperty({ example: 'alice@streple.com' })
  @IsEmail()
  email: string;
}

export interface recaptchaResponse {
  success: true | false;
  challenge_ts: Date;
  hostname: string;
  'error-codes'?: any[];
}
