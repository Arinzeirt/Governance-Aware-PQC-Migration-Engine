import { AuthUser } from '@app/common';
import { category } from '@app/wallets/input';
import { CreateTransferTransactionForDeveloperResponseData } from '@circle-fin/developer-controlled-wallets';

export interface paymentInput {
  user: AuthUser;
  amount: number;
  category: category;
  symbol?: string;
}
export interface paymentResponse {
  response: CreateTransferTransactionForDeveloperResponseData | undefined;
  current: number;
  previous: number;
}

export interface notification {
  email: string;
  amount: string;
  sign: 'USDC' | 'NGN';
  accountNumber: string;
  dateAndTime: Date;
  balance: string;
}
