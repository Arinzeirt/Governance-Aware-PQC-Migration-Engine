import { FindMany, FindOne, transform } from '@app/common';
import { ApiProperty, ApiPropertyOptional, PartialType } from '@nestjs/swagger';
import { CategoryV5 } from 'bybit-api';
import { Transform, Type } from 'class-transformer';
import {
  IsBoolean,
  IsDate,
  IsEnum,
  IsIn,
  IsNotEmpty,
  IsNumber,
  IsObject,
  IsOptional,
  IsString,
  IsUppercase,
  IsUUID,
  Min,
  ValidateNested,
} from 'class-validator';
import {
  copiers,
  copyTrading,
  createTrade,
  duration,
  findManyTrade,
  findOneTrade,
  orderType,
  outcome,
  positionSize,
  riskLevel,
  status,
  type,
} from './traders.interface';

export class followTrader {}

class PositionSize implements positionSize {
  @IsNumber(
    { allowNaN: false, allowInfinity: false },
    { message: 'stakeAmount must be a valid number' },
  )
  @ApiProperty({ type: Number })
  @Transform(({ value }: { value: string | number }) =>
    typeof value === 'string' ? parseFloat(value) : value,
  )
  amount: number;

  @IsString()
  @IsIn(['USDT', 'BTC'])
  @ApiProperty({ type: String, enum: ['USDT', 'BTC'] })
  currency: 'USDT' | 'BTC';
}
export class CreateTrade implements createTrade {
  @IsString()
  @IsNotEmpty()
  @ApiProperty({ type: String })
  asset: string;

  @IsNumber()
  @ApiProperty({ type: Number })
  @Transform(({ value }: { value: string | number }) =>
    typeof value === 'string' ? parseFloat(value) : value,
  )
  leverage: number;

  @IsObject()
  @Type(() => PositionSize)
  @ValidateNested({ each: true })
  @ApiProperty({ type: PositionSize })
  positionSize: positionSize;

  @IsString()
  @IsIn(Object.values(duration))
  @ApiProperty({ type: String, enum: Object.values(duration) })
  duration: duration;

  @IsString()
  @IsIn(['spot', 'linear', 'inverse'])
  @IsEnum(['spot', 'linear', 'inverse'])
  @ApiPropertyOptional({ type: 'string', enum: ['spot', 'linear', 'inverse'] })
  category: CategoryV5 = 'linear';

  @IsString()
  @IsOptional()
  @ApiPropertyOptional({ type: String })
  comment?: string;

  @IsDate()
  @IsOptional()
  @ApiPropertyOptional({ type: Date })
  @Transform(({ value }: { value: string }) =>
    typeof value === 'string' ? new Date(value) : value,
  )
  startDate: Date;

  @IsDate()
  @IsOptional()
  @ApiPropertyOptional({ type: Date })
  @Transform(({ value }: { value: string }) =>
    typeof value === 'string' ? new Date(value) : value,
  )
  expiresAt: Date;

  @IsNumber()
  @IsOptional()
  @ApiProperty({ type: Number })
  @Transform(({ value }: { value: string | number }) =>
    typeof value === 'string' ? parseFloat(value) : value,
  )
  entryPrice: number;

  @IsNumber(
    { allowNaN: false, allowInfinity: false },
    { message: 'stakeAmount must be a valid number' },
  )
  @ApiProperty({ type: Number })
  @Transform(({ value }: { value: string | number }) =>
    typeof value === 'string' ? parseFloat(value) : value,
  )
  stopLoss: number;

  @IsNumber(
    { allowNaN: false, allowInfinity: false },
    { message: 'stakeAmount must be a valid number' },
  )
  @ApiProperty({ type: Number })
  @Transform(({ value }: { value: string | number }) =>
    typeof value === 'string' ? parseFloat(value) : value,
  )
  takeProfit: number;

  @IsBoolean()
  @Transform(({ value }) => {
    if (value === 'true' || value === true) return true;
    if (value === 'false' || value === false) return false;
    if (value === 'yes') return true;
    if (value === 'no') return false;
    return false;
  })
  @ApiProperty({ type: Boolean })
  isDraft: boolean;

  @IsString()
  @ApiProperty({ type: String, enum: ['Buy', 'Sell'] })
  @IsIn(['Buy', 'Sell'])
  action: 'Buy' | 'Sell';

  @IsString()
  @IsIn(Object.values(orderType))
  @ApiProperty({ type: String, enum: Object.values(orderType) })
  orderType: orderType;

  @IsNumber()
  @IsOptional()
  @ApiProperty({ type: Number })
  @Transform(({ value }: { value: string | number }) =>
    typeof value === 'string' ? parseFloat(value) : value,
  )
  minCopiesAmount?: number;
}

export class UpdateTrade extends PartialType(CreateTrade) {}

export class FindManyTrade extends FindMany implements findManyTrade {
  @IsOptional()
  @ApiPropertyOptional({ type: [String], format: 'uuid' })
  @IsString({ each: true })
  @IsUUID('all', { each: true })
  @Transform(({ value }: { value: transform }) =>
    typeof value === 'string' ? [value] : value,
  )
  creatorId?: string[];

  @IsOptional()
  @ApiPropertyOptional({ type: [String], format: 'uuid' })
  @IsString({ each: true })
  @IsUUID('all', { each: true })
  @Transform(({ value }: { value: transform }) =>
    typeof value === 'string' ? [value] : value,
  )
  userId?: string[];

  @IsOptional()
  @ApiPropertyOptional({ type: [String] })
  @IsString({ each: true })
  @Transform(({ value }: { value: transform }) =>
    typeof value === 'string' ? [value] : value,
  )
  symbol?: string[];

  @IsOptional()
  @IsString()
  @IsIn(Object.values(status))
  @ApiPropertyOptional({ type: String, enum: Object.values(status) })
  status?: status;

  @IsOptional()
  @IsString()
  @ApiPropertyOptional({ type: String, enum: Object.values(type) })
  type?: type;

  @IsOptional()
  @IsBoolean()
  @ApiPropertyOptional({ type: Boolean })
  @Transform(({ value }: { value: string | boolean }) => {
    if (value === 'true' || value === true) return true;
    if (value === 'false' || value === false) return false;
    if (value === 'yes') return true;
    if (value === 'no') return false;
    return value;
  })
  draft?: boolean;

  @IsOptional()
  @IsString({ each: true })
  @IsIn(['Buy', 'Sell'], { each: true })
  @Transform(({ value }: { value: transform }) =>
    typeof value === 'string' ? [value] : value,
  )
  @ApiPropertyOptional({ type: [String], enum: ['Buy', 'Sell'] })
  action?: 'Buy' | 'Sell';

  @IsOptional()
  @IsString({ each: true })
  @Transform(({ value }: { value: transform }) =>
    typeof value === 'string' ? [value] : value,
  )
  @ApiPropertyOptional({ type: [String] })
  asset?: string[];

  @IsOptional()
  @IsString({ each: true })
  @IsIn(Object.values(outcome), { each: true })
  @Transform(({ value }: { value: transform }) =>
    typeof value === 'string' ? [value] : value,
  )
  @ApiPropertyOptional({ type: [String], enum: Object.values(outcome) })
  outcome?: outcome[];

  @IsOptional()
  @IsString()
  @IsIn(Object.values(copiers))
  @ApiPropertyOptional({ type: String, enum: Object.values(copiers) })
  copiers?: copiers;

  @IsDate()
  @IsOptional()
  @ApiPropertyOptional({ type: Date })
  @Transform(({ value }: { value: string | Date }) =>
    typeof value === 'string' ? new Date(value) : value,
  )
  fromDate?: Date;

  @IsDate()
  @IsOptional()
  @ApiPropertyOptional({ type: Date })
  @Transform(({ value }: { value: string | Date }) =>
    typeof value === 'string' ? new Date(value) : value,
  )
  toDate?: Date;

  @IsString()
  @IsOptional()
  @IsIn(['top7days', 'last7days', 'last30days', 'last3months'])
  @ApiPropertyOptional({
    type: String,
    enum: ['top7days', 'last7days', 'last30days', 'last3months'],
  })
  timeFrame: string;

  @IsString()
  @IsOptional()
  @IsIn(['0-10', '10-30', '30'])
  @ApiPropertyOptional({
    type: String,
    enum: ['0-10', '10-30', '30'],
  })
  roiRange: string;

  @IsString()
  @IsOptional()
  @IsIn(Object.values(riskLevel))
  @ApiPropertyOptional({
    type: String,
    enum: Object.values(riskLevel),
  })
  riskLevel: riskLevel;

  @IsBoolean()
  @IsOptional()
  @ApiPropertyOptional({ type: Boolean })
  @Transform(({ value }: { value: string | boolean }) => {
    if (value === 'true' || value === true) return true;
    if (value === 'false' || value === false) return false;
    return value;
  })
  tradingTrade: boolean;
}

export class FindOneTrade extends FindOne implements findOneTrade {
  @IsUUID()
  @IsOptional()
  @ApiPropertyOptional({ type: String, format: 'uuid' })
  creatorId?: string;

  @IsUUID()
  @IsOptional()
  @ApiPropertyOptional({ type: String, format: 'uuid' })
  userId?: string;

  @IsString()
  @IsOptional()
  @ApiPropertyOptional({ type: String })
  symbol?: string;

  @IsString()
  @IsOptional()
  @IsIn(Object.values(status))
  @ApiPropertyOptional({ type: String, enum: Object.values(status) })
  status?: status;

  @IsString()
  @IsOptional()
  @IsIn(['Buy', 'Sell'])
  @ApiPropertyOptional({ type: String, enum: ['Buy', 'Sell'] })
  action?: 'Buy' | 'Sell';

  @IsString()
  @IsOptional()
  @ApiPropertyOptional({ type: String })
  asset?: string;

  @IsString()
  @IsOptional()
  @IsIn(Object.values(outcome))
  @ApiPropertyOptional({ type: String, enum: Object.values(outcome) })
  outcome?: outcome;

  @IsString()
  @IsOptional()
  @IsIn(Object.values(copiers))
  @ApiPropertyOptional({ type: String, enum: Object.values(copiers) })
  copiers?: copiers;

  @IsOptional()
  @IsString()
  @ApiPropertyOptional({ type: String, enum: Object.values(type) })
  tradeType?: type;

  @IsOptional()
  @IsBoolean()
  @ApiPropertyOptional({ type: Boolean })
  @Transform(({ value }: { value: string | boolean }) => {
    if (value === 'true' || value === true) return true;
    if (value === 'false' || value === false) return false;
    if (value === 'yes') return true;
    if (value === 'no') return false;
    return value;
  })
  draft?: boolean;
}

export class CopyTrading implements copyTrading {
  @IsUUID()
  @IsString()
  @IsOptional()
  @ApiProperty({ type: String, format: 'uuid' })
  tradeId: string;

  @IsNumber(
    { allowNaN: false, allowInfinity: false },
    { message: 'stakeAmount must be a valid number' },
  )
  @ApiProperty({ type: Number })
  @Min(10)
  @Transform(({ value }: { value: string | number }) =>
    typeof value === 'string' ? parseFloat(value) : value,
  )
  amount: number;
}

export class Parameter {
  @IsUUID()
  @IsString()
  @ApiProperty({ type: String, format: 'uuid' })
  tradeId: string;
}

export class Symbol {
  @IsString()
  @IsNotEmpty()
  @IsUppercase()
  @ApiProperty({ type: String, example: 'BTC/USDT' })
  asset: string;
}
