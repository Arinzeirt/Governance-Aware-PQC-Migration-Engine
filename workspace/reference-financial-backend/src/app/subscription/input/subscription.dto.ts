import { FindMany, FindOne } from '@app/common';
import { ApiProperty, ApiPropertyOptional, PartialType } from '@nestjs/swagger';
import { Transform, Type } from 'class-transformer';
import {
  IsArray,
  IsNotEmpty,
  IsNumber,
  IsOptional,
  IsString,
  IsUUID,
} from 'class-validator';
import {
  findManySubHistory,
  findOneSubHistory,
} from './subscription-history.interface';
import {
  createSubPlan,
  Period,
  PlanName,
  subscribe,
} from './subscription.interface';

export class FindManyHistory extends FindMany implements findManySubHistory {}

export class FindOneHistory extends FindOne implements findOneSubHistory {}

export class CreateSubscription implements subscribe {
  @IsUUID()
  @IsString()
  @IsNotEmpty()
  @ApiProperty({ type: String, format: 'uuid' })
  planId: string;
}

export class CreatePlan implements createSubPlan {
  @IsString()
  @IsNotEmpty()
  @ApiProperty({ type: String })
  name: PlanName;

  @IsNumber()
  @IsNotEmpty()
  @ApiProperty({ type: Number })
  @Transform(({ value }) =>
    typeof value === 'string' ? parseFloat(value) : value,
  )
  price: number;

  @IsString()
  @IsNotEmpty()
  @ApiProperty({
    type: String,
    enum: Object.values(Period),
    example: Period.month,
  })
  period: Period;

  @IsArray()
  @IsOptional()
  @Type(() => String)
  @IsString({ each: true })
  @ApiPropertyOptional({ type: [String] })
  features?: string[];
}

export class UpdatePlan
  extends PartialType(CreatePlan)
  implements Partial<createSubPlan> {}

export class CancelSubscription {
  @IsString()
  @IsOptional()
  @ApiPropertyOptional({ type: String })
  reason: string;
}
