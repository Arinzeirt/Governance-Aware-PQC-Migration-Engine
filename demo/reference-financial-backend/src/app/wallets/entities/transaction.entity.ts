import {
  Column,
  CreateDateColumn,
  Entity,
  Index,
  JoinColumn,
  ManyToOne,
  PrimaryGeneratedColumn,
  UpdateDateColumn,
} from 'typeorm';
import {
  category,
  ITransaction,
  IWallets,
  transactionStatus,
  transactionType,
} from '../input';
import { Wallets } from './wallet.entity';
import { User } from '@app/users/entity';
import { billsTransaction } from '@app/utilities/input';
import { BillTnx } from '@app/utilities/entities';

@Entity('transactions')
export class Transaction implements ITransaction {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @ManyToOne(() => Wallets, (wallet) => wallet.transactions, {
    onDelete: 'SET NULL',
    nullable: true,
  })
  @JoinColumn({ name: 'walletId' })
  wallet?: IWallets;

  @Index()
  @Column({ type: 'enum', enum: Object.values(transactionType) })
  type: transactionType;

  @Column({ type: 'decimal', precision: 18, scale: 8 })
  amount: number;

  @Index()
  @Column({ nullable: true, unique: true })
  idempotency?: string;

  @Column({ type: 'decimal', precision: 18, scale: 8 })
  previousBal: number;

  @Column({ type: 'decimal', precision: 18, scale: 8 })
  currentBal: number;

  // who received the transaction (optional for deposits)
  @ManyToOne(() => User, { onDelete: 'SET NULL', nullable: true })
  recipient?: User;

  @Index()
  @Column({ type: 'uuid', nullable: true })
  userId: string;

  // who initiated the transaction
  @ManyToOne(() => User, { onDelete: 'SET NULL', nullable: true })
  user: User;

  @Index()
  @Column({ nullable: false })
  reference: string;

  @ManyToOne(() => BillTnx, (tnx) => tnx.id, {
    onDelete: 'SET NULL',
    nullable: true,
  })
  @JoinColumn({ name: 'billId' })
  bills?: billsTransaction;

  @Column({ nullable: true })
  description: string;

  @Index()
  @Column({
    type: 'enum',
    enum: Object.values(category),
    default: category.others,
  })
  category: category;

  @Index()
  @Column({ nullable: true })
  externalRef?: string;

  @Index()
  @Column({ nullable: true })
  txHash?: string;

  @Column({ nullable: true })
  userOpHash?: string;

  @Column({ nullable: true })
  errorDetails?: string;

  @Column({ nullable: true })
  networkFee?: string;

  @Index()
  @Column({
    type: 'enum',
    enum: Object.values(transactionStatus),
  })
  status: transactionStatus;

  @Index()
  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
