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
import { SubPlan, Subscriptions, SubscriptionStatus } from '../input';
import { SubPlans } from './plan.entity';

@Entity('subscriptions')
export class Subscription implements Subscriptions {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @ManyToOne(() => User, (user) => user.subscriptions, {
    onDelete: 'SET NULL',
    nullable: true,
  })
  @JoinColumn({ name: 'userId' })
  user: User;

  @ManyToOne(() => SubPlans, { onDelete: 'SET NULL', nullable: true })
  @JoinColumn({ name: 'planId' })
  plan: SubPlan;

  @Column({
    type: 'enum',
    nullable: false,
    enum: Object.values(SubscriptionStatus),
  })
  status: SubscriptionStatus;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
