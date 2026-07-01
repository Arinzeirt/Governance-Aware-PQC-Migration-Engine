import { IUser } from './user.interface';

export interface IUserActivity {
  id: string;
  user: IUser;
  date: string;
  createdAt: Date;
  updatedAt: Date;
}
