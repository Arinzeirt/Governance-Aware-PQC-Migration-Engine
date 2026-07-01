import { User } from '@app/users/entity';
import {
  Column,
  CreateDateColumn,
  Entity,
  Index,
  ManyToOne,
  PrimaryGeneratedColumn,
  UpdateDateColumn,
} from 'typeorm';
import {
  duration,
  ITrades,
  orderType,
  outcome,
  positionSize,
  riskLevel,
  status,
  type,
} from '../input';
import { CategoryV5 } from 'bybit-api';

@Entity()
export class Trades implements ITrades {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @ManyToOne(() => User, { onDelete: 'SET NULL', nullable: true })
  user: User;

  @Index()
  @Column({ type: 'uuid', nullable: true })
  userId: string;

  @ManyToOne(() => User, { onDelete: 'SET NULL', nullable: true })
  creator: User;

  @Index()
  @Column({ type: 'uuid', nullable: false })
  creatorId: string;

  @Column({ default: 'linear' })
  category: CategoryV5;

  @Index() @Column() symbol: string;

  @Column('float') stopLoss: number;
  @Column('float') takeProfit: number;

  @Index()
  @Column({
    type: 'enum',
    enum: Object.values(status),
    nullable: false,
    default: status.pending,
  })
  status: status;

  @Column({ type: 'float', nullable: true })
  exitPrice: number;

  @Index()
  @Column({ nullable: false, default: 'Buy' })
  action: 'Buy' | 'Sell';

  @Column({ type: 'float', nullable: false, default: 0 })
  margin: number;

  @Index()
  @Column({
    type: 'enum',
    enum: Object.values(type),
    nullable: false,
    default: type.copy,
  })
  tradeType: type;

  @Index()
  @Column({ nullable: false })
  identifier: string;

  @Index()
  @Column()
  asset: string;

  @Column({ type: 'float', nullable: true })
  entryPrice: number;

  @Column()
  leverage: number;

  @Column({ type: 'enum', enum: Object.values(outcome), nullable: true })
  outcome?: outcome;

  @Column({ type: 'float', nullable: false, default: 0 })
  tradeRoi: number;

  @Column({ type: 'float', nullable: false, default: 0 })
  currentPrice: number;

  @Index()
  @Column({ nullable: true })
  orderLinkId: string;

  @Column({ nullable: true })
  orderId?: string;

  @Column({ nullable: true })
  errorMsg?: string;

  @Column({ type: 'jsonb', default: { amount: 0, currency: 'USDT' } })
  positionSize: positionSize;

  @Column({ type: 'float', default: 0 })
  realizedPnl: number;

  @Column({ type: 'int', nullable: false, default: 0 })
  noOfCopiers: number;

  @Column({ type: 'int', nullable: false, default: 0 })
  scheduleStartId?: number;

  @Column({ type: 'int', nullable: false, default: 0 })
  scheduleEndId?: number;

  @Column({ type: 'enum', enum: Object.values(duration) })
  duration: duration;

  @Column({ type: 'timestamp', default: () => 'now()' })
  startDate: Date;

  @Column({ type: 'timestamp', default: () => 'now()' })
  expiresAt: Date;

  @Column({
    type: 'enum',
    enum: Object.values(riskLevel),
    default: riskLevel.low,
  })
  riskLevel: riskLevel;

  @Index()
  @Column({ type: 'boolean', default: false })
  isDraft: boolean;

  @Index()
  @Column({
    type: 'enum',
    enum: Object.values(orderType),
    default: orderType.limit,
  })
  orderType: orderType;

  @Index()
  @Column({ nullable: true })
  fundId?: string;

  @Column({ nullable: true })
  image?: string;

  @Column({ nullable: true })
  comment?: string;

  @Column({ type: 'int', nullable: true, default: 0 })
  risk_reward_score?: number;

  @Column({ type: 'int', nullable: true, default: 0 })
  trend_alignment_score?: number;

  @Column({ type: 'int', nullable: true, default: 0 })
  liquidity_score?: number;

  @Column({ type: 'int', nullable: true, default: 0 })
  volatility_risk_score?: number;

  @Column({ type: 'int', nullable: true, default: 0 })
  entry_quality_score?: number;

  @Column({ type: 'int', nullable: true, default: 0 })
  timing_score?: number;

  @Column({ type: 'int', nullable: true, default: 0 })
  leverage_risk_score?: number;

  @Column({ type: 'int', nullable: true, default: 0 })
  overall_score?: number;

  @Column({ nullable: true, default: '' })
  reasoning?: string;

  @Column({ nullable: true, default: '' })
  suggestions?: string;

  @Column({ type: 'float', nullable: true, default: 0 })
  minCopiesAmount?: number;

  @Index()
  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;

  getTotalProfitForCopies(): number {
    if (this.tradeRoi > 0) {
      return this.margin * this.tradeRoi * this.noOfCopiers;
    }
    return 0;
  }
}
