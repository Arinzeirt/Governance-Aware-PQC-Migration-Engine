import { ApiProperty } from '@nestjs/swagger';
import {
  IsBoolean,
  IsEnum,
  IsNotEmpty,
  IsNumber,
  IsString,
  IsUUID,
  Max,
  Min,
} from 'class-validator';
import { copySetting } from './copy-setting.interface';
import { Transform } from 'class-transformer';

export class CopySettings implements copySetting {
  @IsNotEmpty()
  @IsString()
  @IsUUID()
  @ApiProperty({
    type: 'string',
    format: 'uuid',
    example: 'a1b2c3d4-e5f6-7890-1234-567890abcdef',
  })
  traderId: string;

  @IsNotEmpty()
  @IsNumber()
  @Min(1)
  @Max(2000)
  @ApiProperty({ type: 'number', example: 100 })
  @Transform(({ value }) =>
    typeof value === 'string' ? parseFloat(value) : value,
  )
  amount: number;

  @IsNotEmpty()
  @IsEnum(['Proportional', 'Fixed'])
  @ApiProperty({
    type: 'string',
    enum: ['Proportional', 'Fixed'],
    example: 'Proportional',
  })
  copyMode: 'Proportional' | 'Fixed';

  @IsNotEmpty()
  @IsNumber()
  @Min(0.5)
  @Max(2)
  @ApiProperty({ type: 'number', example: 1 })
  @Transform(({ value }) =>
    typeof value === 'string' ? parseFloat(value) : value,
  )
  copyRatio: number;

  @IsNotEmpty()
  @IsNumber()
  @ApiProperty({ type: 'number', example: 100 })
  @Transform(({ value }) =>
    typeof value === 'string' ? parseFloat(value) : value,
  )
  stopCopying: number;

  @IsNotEmpty()
  @IsBoolean()
  @ApiProperty({ type: 'boolean', example: true })
  @Transform(({ value }) => {
    if (value === 'true' || value === true || value === 1) return true;
    if (value === 'false' || value === false || value === 0) return false;
    return value;
  })
  autoClose: boolean;
}
