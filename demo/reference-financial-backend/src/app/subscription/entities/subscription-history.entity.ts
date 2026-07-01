import { User } from '@app/users/entity';
import {
  Column,
  CreateDateColumn,
  Entity,
  JoinColumn,
  ManyToOne,
  PrimaryGeneratedColumn,
  UpdateDateColumn,
} from 'typeorm';
import { IHistory, SubPlan, SubscriptionStatus } from '../input';
import { SubPlans } from './plan.entity';

@Entity('subscription_history')
export class SubscriptionHistory implements IHistory {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @ManyToOne(() => User, { onDelete: 'SET NULL', nullable: true })
  @JoinColumn({ name: 'userId' })
  user: User;

  @ManyToOne(() => SubPlans, { onDelete: 'SET NULL', nullable: true })
  @JoinColumn({ name: 'planId' })
  plan: SubPlan;

  @Column({ nullable: true })
  paymentId?: string;

  @Column({ type: 'timestamp', nullable: false })
  startingDate: Date;

  @Column({ type: 'timestamp', nullable: false })
  expiringDate: Date;

  @Column({ type: 'decimal', precision: 10, scale: 2 })
  price: number;

  @Column({ type: 'integer', nullable: true })
  scheduleId?: number;

  @Column({ type: 'text', nullable: true })
  changeReason: string;

  @Column({
    type: 'enum',
    enum: SubscriptionStatus,
    default: SubscriptionStatus.pending,
  })
  status: SubscriptionStatus;

  @Column({ type: 'jsonb', nullable: true })
  metadata: Record<string, any>;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
