import {
  IsIn,
  IsNotEmpty,
  IsNumber,
  IsString,
  IsUUID,
  MaxLength,
  MinLength,
} from 'class-validator';
import {
  electricityPayload,
  getData,
  IAirtime,
  IData,
  metercode,
  network,
  verifyMeterName,
} from './utility.interface';
import { Transform } from 'class-transformer';
import { ApiProperty, PickType } from '@nestjs/swagger';

const code = [
  'mtn-data',
  'airtel-data',
  'glo-data',
  'glo-sme-data',
  'etisalat-data',
  'smile-direct',
  'spectranet',
];

export class Airtime implements IAirtime {
  @IsString()
  @IsNotEmpty()
  @ApiProperty({ type: String })
  phone: string;

  @IsNumber()
  @IsNotEmpty()
  @ApiProperty({ type: Number })
  @Transform(({ value }: { value: string }) =>
    typeof value === 'string' ? parseFloat(value) : value,
  )
  amount: number;

  @IsUUID()
  @IsString()
  @IsNotEmpty()
  @ApiProperty({ type: String })
  idempotency: string;

  @IsString()
  @IsNotEmpty()
  @MaxLength(4)
  @MinLength(4)
  @ApiProperty({ type: String })
  pin: string;

  @IsString()
  @IsNotEmpty()
  @IsIn(Object.values(network))
  @ApiProperty({ type: String, enum: Object.values(network) })
  serviceID: network;
}

export class Data
  extends PickType(Airtime, ['phone', 'pin', 'serviceID', 'idempotency'])
  implements IData
{
  @IsString()
  @IsNotEmpty()
  variation_code: string;

  @IsString()
  @IsNotEmpty()
  @IsIn(code)
  @ApiProperty({ type: String, enum: code })
  networkCode:
    | 'mtn-data'
    | 'airtel-data'
    | 'glo-data'
    | 'glo-sme-data'
    | 'etisalat-data'
    | 'smile-direct'
    | 'spectranet';
}

export class DataBundle implements getData {
  @IsString()
  @IsNotEmpty()
  @IsIn(code)
  @ApiProperty({ type: String, enum: code })
  code:
    | 'mtn-data'
    | 'airtel-data'
    | 'glo-data'
    | 'glo-sme-data'
    | 'etisalat-data'
    | 'smile-direct'
    | 'spectranet';
}

export class Electricity
  extends PickType(Airtime, ['pin', 'amount', 'idempotency', 'phone'])
  implements electricityPayload
{
  @IsString()
  @IsNotEmpty()
  @IsIn(Object.values(metercode))
  @ApiProperty({ type: String, enum: Object.values(metercode) })
  serviceID: metercode;

  @IsString()
  @IsNotEmpty()
  @ApiProperty({ type: String })
  billersCode: string;

  @IsString()
  @IsNotEmpty()
  @IsIn(['prepaid', 'postpaid'])
  @ApiProperty({ type: String, enum: ['prepaid', 'postpaid'] })
  type: 'prepaid' | 'postpaid';
}

export class VerifyElectricityName
  extends PickType(Electricity, ['billersCode', 'serviceID', 'type'])
  implements verifyMeterName {}
