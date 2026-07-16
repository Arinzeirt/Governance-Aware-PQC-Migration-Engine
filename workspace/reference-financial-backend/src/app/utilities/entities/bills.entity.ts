import {
  Column,
  CreateDateColumn,
  Entity,
  PrimaryGeneratedColumn,
  UpdateDateColumn,
} from 'typeorm';
import { billsTransaction, billType } from '../input';

@Entity('bill_transactions')
export class BillTnx implements billsTransaction {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ nullable: true })
  bundleSize?: string;

  @Column({ type: 'enum', enum: billType })
  category: billType;

  @Column({ type: 'json', nullable: false })
  payload: Record<string, string | number>;

  @Column({ nullable: true })
  type?: string;

  // electricity
  @Column({ nullable: true })
  customerName?: string;

  @Column({ nullable: true })
  meterToken?: string;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
