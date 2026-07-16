import { category } from '@app/wallets/input';

export enum network {
  mtn = 'mtn',
  glo = 'glo',
  air = 'airtel',
  mob = 'etisalat',
}

export interface IAirtime {
  phone: string;
  amount: number;
  idempotency: string;
  pin: string;
  serviceID: network;
  request_id?: string;
}

export interface requery {
  request_id: string;
  createdAt: Date;
}

export interface getData {
  code:
    | 'mtn-data'
    | 'airtel-data'
    | 'glo-data'
    | 'glo-sme-data'
    | 'etisalat-data'
    | 'smile-direct'
    | 'spectranet';
}

export interface utilityResponse {
  code: string;
  content: {
    transactions: {
      status: string;
      product_name: string;
      unique_element: string;
      unit_price: string;
      quantity: number;
      service_verification: string | null;
      channel: string;
      commission: string;
      total_amount: number;
      discount: string | null;
      type: string;
      email: string;
      phone: string;
      name: string | null;
      convinience_fee: number;
      amount: string;
      platform: string;
      method: string;
      transactionId: string;
      commission_details: {
        amount: number;
        rate: string;
        rate_type: string;
        computation_type: string;
      };
    };
  };
  response_description: string;
  requestId: string;
  amount: number;
  transaction_date: string;
  purchased_code: string;
  customerName: string | null;
  customerAddress: string | null;
  exchangeReference: string;
  mainToken: string;
  mainTokenDescription: string;
  mainTokenUnits: string | null;
  mainTokenTax: number;
  mainsTokenAmount: number;
  bonusToken: string | null;
  bonusTokenDescription: string | null;
  bonusTokenUnits: string | null;
  bonusTokenTax: string | null;
  bonusTokenAmount: string | null;
  tariffIndex: string;
  debtTariff: string | null;
  debtAmount: string | null;
  debtDescription: string | null;
  KCT1: string;
  KCT2: string;
}

export interface varations {
  variation_code: string;
  name: string;
  variation_amount: string;
  fixedPrice: string;
  duration?: string;
  bundleSize?: string;
}

export interface dataResponse {
  response_description: string;
  content: {
    ServiceName: string;
    serviceID: string;
    convinience_fee: string;
    variations: varations[];
    varations: varations[];
  };
}

export interface IData extends Pick<IAirtime, 'pin' | 'idempotency'> {
  phone: string;
  serviceID: network;
  billersCode?: string;
  request_id?: string;
  variation_code: string;
  amount?: string;
  networkCode:
    | 'mtn-data'
    | 'airtel-data'
    | 'glo-data'
    | 'glo-sme-data'
    | 'etisalat-data'
    | 'smile-direct'
    | 'spectranet';
}

export enum metercode {
  eko = 'eko-electric',
  ikeja = 'ikeja-electric',
  kano = 'kano-electric',
  port = 'portharcourt-electric',
  jos = 'jos-electric',
  ibadan = 'ibadan-electric',
  kaduna = 'kaduna-electric',
  abuja = 'abuja-electric',
  enugu = 'enugu-electric',
  benin = 'benin-electric',
  aba = 'aba-electric',
  yola = 'yola-electric',
}

export interface verifyMeterName {
  billersCode: string;
  serviceID: metercode;
  type: 'prepaid' | 'postpaid';
}

export interface verifyResponse {
  code: string;
  content: {
    Customer_Name: string;
    Address: string;
    Meter_Number: string;
    Customer_Arrears: string;
    Minimum_Amount: string;
    Min_Purchase_Amount: string;
    Can_Vend: string;
    Business_Unit: string;
    Customer_Account_Type: string;
    Meter_Type: string;
    WrongBillersCode: boolean;
    commission_details: {
      amount: number | null;
      rate: string;
      rate_type: string;
      computation_type: string;
    };
  };
}

export interface electricityPayload extends Pick<
  IAirtime,
  'pin' | 'idempotency'
> {
  request_id?: string;
  serviceID: metercode;
  billersCode: string;
  variation_code?: 'prepaid' | 'postpaid';
  type: 'prepaid' | 'postpaid';
  amount: number;
  phone: string;
}

export interface processPayment {
  idempotency: string;
  amount: number;
  service: category;
}

export enum billType {
  airtime = 'airtime',
  data = 'data',
  electricity = 'electricity',
}
export interface billsTransaction {
  id: string;
  category: billType;
  type?: string; //SME, Direct, prepaid, postpaid e.t.c
  payload: Record<string, string | number>;
  customerName?: string;
  meterToken?: string;
  bundleSize?: string; //MB OR GB
  createdAt: Date;
  updatedAt: Date;
}

export type createBill = Omit<
  billsTransaction,
  'id' | 'createdAt' | 'updatedAt'
>;
