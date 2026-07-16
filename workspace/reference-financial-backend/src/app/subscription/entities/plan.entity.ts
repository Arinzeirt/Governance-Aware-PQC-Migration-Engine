import {
  Column,
  CreateDateColumn,
  Entity,
  PrimaryGeneratedColumn,
  UpdateDateColumn,
} from 'typeorm';
import { Period, PlanName, SubPlan } from '../input';

@Entity('subscription-plans')
export class SubPlans implements SubPlan {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({
    type: 'enum',
    enum: Object.values(PlanName),
    default: PlanName.free,
  })
  name: PlanName;

  @Column({ type: 'enum', enum: Object.values(Period), default: Period.week })
  period: Period;

  @Column({ type: 'jsonb', nullable: true })
  features?: string[];

  @Column({ type: 'decimal', precision: 10, scale: 2 })
  price: number;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
