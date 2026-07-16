import { IUser } from '@app/users/interface';

export interface ICopySettings {
  id: string;
  user: IUser;
  trader: IUser;
  amount: number;
  copyMode: 'Proportional' | 'Fixed';
  copyRatio: number;
  stopCopying: number;
  autoClose: boolean;
  createdAt: Date;
  updatedAt: Date;
}

export interface copySetting extends Omit<
  ICopySettings,
  'id' | 'user' | 'trader' | 'createdAt' | 'updatedAt'
> {
  traderId: string;
}
