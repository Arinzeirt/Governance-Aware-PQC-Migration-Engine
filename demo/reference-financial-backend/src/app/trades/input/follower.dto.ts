import { FindMany } from '@app/common';
import { ApiProperty, ApiPropertyOptional, PickType } from '@nestjs/swagger';
import { Transform } from 'class-transformer';
import { IsIn, IsInt, IsOptional, IsString, IsUUID } from 'class-validator';
import {
  createFollower,
  curve,
  getAllFollowing,
  Period,
  profilePerformance,
} from './follower.interface';

export class CreateFollower implements createFollower {
  @IsUUID()
  @IsString()
  @ApiProperty({ type: String, format: 'uuid' })
  followingId: string;
}

export class ProfilePerformance implements profilePerformance {
  @IsString()
  @IsOptional()
  @IsIn(['daily', '7D', '30D', '90D', '1YR', '2YR'])
  @ApiPropertyOptional({
    type: String,
    enum: ['daily', '7D', '30D', '90D', '1YR', '2YR'],
  })
  period: Period = 'daily';

  @IsUUID()
  @IsString()
  @ApiProperty({ type: String, format: 'uuid' })
  userId: string;
}

export class CopierProfilePerformance extends PickType(ProfilePerformance, [
  'period',
]) {}

export class Curve implements curve {
  @IsInt()
  @IsOptional()
  @ApiPropertyOptional({ type: Number })
  @Transform(({ value }: { value: string }) =>
    typeof value === 'string' ? parseInt(value) : value,
  )
  period: number = 7;

  @IsUUID()
  @IsString()
  @ApiProperty({ type: String, format: 'uuid' })
  userId: string;
}

export class GetAllFollowing extends FindMany implements getAllFollowing {
  @IsOptional()
  @IsString({ each: true })
  @IsUUID('all', { each: true })
  @ApiPropertyOptional({ type: String, format: 'uuid', isArray: true })
  @Transform(({ value }) => (typeof value === 'string' ? [value] : value))
  followerId: string[];

  @IsOptional()
  @IsString({ each: true })
  @IsUUID('all', { each: true })
  @ApiPropertyOptional({ type: String, format: 'uuid', isArray: true })
  @Transform(({ value }) => (typeof value === 'string' ? [value] : value))
  followingId: string[];
}
