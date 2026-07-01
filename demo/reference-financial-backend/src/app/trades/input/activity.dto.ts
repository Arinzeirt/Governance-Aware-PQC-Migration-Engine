import {
  IsInt,
  IsNotEmpty,
  IsNumber,
  IsOptional,
  IsString,
  IsUUID,
  Max,
  Min,
} from 'class-validator';
import { copierInput, findManyActivity } from './activity.interface';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { Transform } from 'class-transformer';

export class FindManyActivity implements findManyActivity {
  @IsOptional()
  @IsString({ each: true })
  @IsUUID('all', { each: true })
  @ApiPropertyOptional({ type: [String] })
  userId?: string[];

  @IsOptional()
  @IsString({ each: true })
  @ApiPropertyOptional({ type: [String] })
  title?: string[];
}

export class CopierBreakdown implements copierInput {
  @IsNotEmpty()
  @IsString()
  @IsUUID()
  @ApiProperty({ type: String })
  traderId: string;

  @Min(1)
  @IsInt()
  @IsOptional()
  @Transform(({ value }: { value: string }) => parseInt(value, 10))
  @ApiPropertyOptional({ type: Number })
  page: number = 1;

  @IsInt()
  @Min(1)
  @Max(100)
  @IsOptional()
  @Transform(({ value }: { value: string }) => parseInt(value, 30))
  @ApiPropertyOptional({ type: Number })
  limit: number = 30;
}
