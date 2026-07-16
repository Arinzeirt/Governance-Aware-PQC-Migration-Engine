import {
  Entity,
  PrimaryGeneratedColumn,
  ManyToOne,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
} from 'typeorm';
import { User } from '@app/users/entity/user.entity';
import { gameProgress, Level, Phase } from '../interface';

@Entity('game_progress')
export class GameProgress implements gameProgress {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ nullable: true })
  userId: string;

  @ManyToOne(() => User, { onDelete: 'SET NULL', nullable: true })
  user: User;

  @Column({ type: 'enum', enum: Phase, nullable: false })
  phase: Phase;

  @Column({ type: 'enum', enum: Level, nullable: false })
  level: Level;

  @Column({ default: 0 })
  score: number;

  @Column({ type: 'decimal', nullable: false, default: 10 })
  earn: number;

  @Column({ type: 'timestamp' })
  completedAt: Date;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
