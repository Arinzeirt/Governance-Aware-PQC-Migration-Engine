import {
  ForbiddenException,
  Injectable,
  InternalServerErrorException,
  NotFoundException,
} from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository, TypeORMError } from 'typeorm';
import { SubPlans } from '../entities';
import { createSubPlan } from '../input';

@Injectable()
export class PlanService {
  constructor(
    @InjectRepository(SubPlans)
    private readonly planRepository: Repository<SubPlans>,
  ) {}

  async createPlan(plan: createSubPlan): Promise<SubPlans> {
    try {
      const findPlan = await this.planRepository.findOne({
        where: {
          name: plan.name,
          period: plan.period,
        },
      });

      if (findPlan) throw new ForbiddenException('Plan already exists');

      const newPlan = this.planRepository.create(plan);
      return this.planRepository.save(newPlan);
    } catch (error) {
      if (error instanceof TypeORMError) {
        throw new InternalServerErrorException();
      }
      throw error;
    }
  }

  async findMany(): Promise<SubPlans[]> {
    try {
      return this.planRepository.find();
    } catch (error) {
      if (error instanceof TypeORMError) {
        throw new InternalServerErrorException();
      }
      throw error;
    }
  }

  async findOne(id: string): Promise<SubPlans> {
    try {
      const plan = await this.planRepository.findOne({ where: { id } });
      if (!plan) throw new NotFoundException('Plan not found');
      return plan;
    } catch (error) {
      if (error instanceof TypeORMError) {
        throw new InternalServerErrorException();
      }
      throw error;
    }
  }

  async update(id: string, payload: Partial<createSubPlan>): Promise<SubPlans> {
    try {
      const plan = await this.planRepository.findOne({ where: { id } });
      if (!plan) throw new NotFoundException('Plan not found');
      return this.planRepository.save({ ...plan, ...payload });
    } catch (error) {
      if (error instanceof TypeORMError) {
        throw new InternalServerErrorException();
      }
      throw error;
    }
  }

  async delete(id: string): Promise<{ message: string }> {
    try {
      const plan = await this.planRepository.findOne({ where: { id } });
      if (!plan) throw new NotFoundException('Plan not found');
      await this.planRepository.delete({ id });
      return { message: 'Plan deleted successfully' };
    } catch (error) {
      if (error instanceof TypeORMError) {
        throw new InternalServerErrorException();
      }
      throw error;
    }
  }
}
