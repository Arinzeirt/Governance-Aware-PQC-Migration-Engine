// users/dto/change-password.dto.ts
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import {
  IsDate,
  IsEmail,
  IsIn,
  IsNotEmpty,
  IsOptional,
  IsString,
  IsStrongPassword,
  MinLength,
} from 'class-validator';
import { dashboardFilter } from '../interface';
import { Transform } from 'class-transformer';

export class ChangePasswordDto {
  @ApiProperty({ example: 'alice@streple.com' })
  @IsEmail()
  email: string;

  @ApiProperty({
    example: 'CurrentP@ssw0rd',
    description: 'Current user password',
  })
  @IsNotEmpty()
  @IsString()
  @MinLength(8)
  currentPassword: string;

  @ApiProperty({
    example: 'NewP@ssw0rd',
    description: 'New desired password, min 8 chars',
  })
  @IsNotEmpty()
  @IsString()
  @IsStrongPassword()
  @MinLength(8)
  newPassword: string;
}

export class DashboardFilter implements dashboardFilter {
  @IsString()
  @IsOptional()
  @IsIn(['this year', 'this week', 'this month'])
  @ApiPropertyOptional({
    type: String,
    enum: ['this year', 'this week', 'this month'],
    example: 'this year',
  })
  range: 'this year' | 'this week' | 'this month' = 'this year';

  @IsDate()
  @IsOptional()
  @Transform(({ value }: { value: string }) =>
    typeof value === 'string' ? new Date(value) : value,
  )
  from?: Date;

  @IsDate()
  @IsOptional()
  @Transform(({ value }: { value: string }) =>
    typeof value === 'string' ? new Date(value) : value,
  )
  to?: Date;
}
