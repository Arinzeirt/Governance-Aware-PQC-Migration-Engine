import {
  Column,
  CreateDateColumn,
  Entity,
  JoinColumn,
  ManyToOne,
  PrimaryGeneratedColumn,
  UpdateDateColumn,
} from 'typeorm';
import { ICopySettings } from '../input';
import { IUser } from '@app/users/interface';
import { User } from '@app/users/entity';

@Entity('copy-settings')
export class CopySettingEntity implements ICopySettings {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @ManyToOne(() => User, { onDelete: 'CASCADE' })
  @JoinColumn({ name: 'userId' })
  user: IUser;

  @ManyToOne(() => User, { onDelete: 'CASCADE' })
  @JoinColumn({ name: 'traderId' })
  trader: IUser;

  @Column({ type: 'decimal', precision: 10, scale: 2 })
  amount: number;

  @Column({ type: 'enum', enum: ['Proportional', 'Fixed'] })
  copyMode: 'Proportional' | 'Fixed';

  @Column({ type: 'decimal', precision: 10, scale: 2 })
  copyRatio: number;

  @Column({ type: 'decimal', precision: 10, scale: 2 })
  stopCopying: number;

  @Column({ type: 'boolean' })
  autoClose: boolean;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
