import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import {
  IsNotEmpty,
  IsOptional,
  IsString,
  IsUUID,
  MaxLength,
  Min,
  MinLength,
} from 'class-validator';
import { nameEnquiry, transferFunds } from './seerbit.interface';

export class NameEnquiry implements nameEnquiry {
  @IsString()
  @IsNotEmpty()
  @MaxLength(10)
  @MinLength(10)
  @ApiProperty({ type: String })
  accountnumber: string;

  @IsString()
  @IsNotEmpty()
  @MinLength(6)
  @ApiProperty({ type: String })
  bankcode: string;
}

export class TransferFunds implements transferFunds {
  @IsOptional()
  @IsString()
  @IsUUID()
  @ApiPropertyOptional({ type: String })
  reference?: string;

  @IsString()
  @IsNotEmpty()
  @Min(100)
  @ApiProperty({ type: String })
  amount: string;

  @IsString()
  @IsOptional()
  @MaxLength(50)
  @ApiProperty({ type: String })
  description: string;

  @IsString()
  @IsNotEmpty()
  @MaxLength(10)
  @MinLength(10)
  @ApiProperty({ type: String })
  accountNumber: string;

  @IsString()
  @IsNotEmpty()
  @MinLength(6)
  @ApiProperty({ type: String })
  bankCode: string;

  @IsString()
  @IsNotEmpty()
  @MaxLength(4)
  @MinLength(4)
  @ApiProperty({ type: String })
  transactionPin: string;
}
