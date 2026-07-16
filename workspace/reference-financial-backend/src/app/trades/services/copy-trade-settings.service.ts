import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { CopySettingEntity } from '../entities/copy-setting.entity';
import { Repository } from 'typeorm';
import { copySetting } from '../input';
import { AuthUser } from '@app/common';
import { UsersService } from '@app/users/service';
import { Role } from '@app/users/interface';

@Injectable()
export class CopyTradeSettingsService {
  constructor(
    @InjectRepository(CopySettingEntity)
    private readonly copySettingRepo: Repository<CopySettingEntity>,
    private readonly userService: UsersService,
  ) {}

  async createCopySetting(copySetting: copySetting, user: AuthUser) {
    const { traderId, ...rest } = copySetting;
    const trader = await this.userService.findOne({
      id: traderId,
      role: Role.pro,
    });
    if (!trader.data) {
      throw new NotFoundException('Trader not found');
    }
    const exists = await this.copySettingRepo.findOne({
      where: {
        user: { id: user.id },
        trader: { id: traderId },
      },
    });

    if (exists) {
      await this.copySettingRepo.update(exists.id, rest);
      return { ...exists, ...rest };
    }

    const copySettingEntity = this.copySettingRepo.create({
      ...rest,
      user: { id: user.id },
      trader: { id: traderId },
    });
    return await this.copySettingRepo.save(copySettingEntity);
  }
}
