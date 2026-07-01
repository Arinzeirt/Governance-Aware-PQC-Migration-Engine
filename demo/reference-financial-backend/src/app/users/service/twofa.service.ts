import { AuthUser } from '@app/common';
import { SecurityService } from '@app/helpers';
import {
  BadRequestException,
  ForbiddenException,
  Injectable,
  NotFoundException,
} from '@nestjs/common';
import { generateSecret, generateURI, verify, createGuardrails } from 'otplib';
import {
  generate2FaPayload,
  initiateTfaEnabling,
  ManageTfa,
} from '../interface';
import { UsersService } from './users.service';

const guardrails = createGuardrails({
  MIN_SECRET_BYTES: 10,
});

@Injectable()
export class TwoFAService {
  constructor(
    private readonly security: SecurityService,
    private readonly userService: UsersService,
  ) {}

  generateTfaSecret(user: AuthUser): generate2FaPayload {
    try {
      const secret = generateSecret({});
      const otpAuthUrl = generateURI({
        issuer: 'Streple',
        label: user.email,
        secret,
      });
      return { uri: otpAuthUrl, secret };
    } catch (error) {
      throw error;
    }
  }

  async verifyTfaCode(secret: string, code: string): Promise<boolean> {
    try {
      const { valid } = await verify({ secret, token: code, guardrails });
      return valid;
    } catch (error) {
      throw error;
    }
  }

  async initiateTfaEnabling({
    email,
    secret,
  }: initiateTfaEnabling): Promise<void> {
    try {
      const user = await this.userService.login(email);
      if (!user) throw new NotFoundException('User not found');

      const tfaSecret = await this.security.encrypt(secret);
      await this.userService.updateProfile({ tfaSecret }, user);
    } catch (error) {
      throw error;
    }
  }

  async enableTfaForUser({
    email,
    tfaToken,
  }: ManageTfa): Promise<{ message: string }> {
    const user = await this.userService.login(email);
    if (!user) {
      throw new NotFoundException('User not found');
    }

    if (user.isTfaEnabled) {
      throw new BadRequestException('TFA is already enabled');
    }

    if (!user.tfaSecret) {
      throw new ForbiddenException('TFA is not enabled for this account');
    }

    const secret = await this.security.decrypt(user.tfaSecret);
    if (!this.verifyTfaCode(secret, tfaToken)) {
      throw new BadRequestException('Invalid TFA token');
    }

    await this.userService.updateProfile({ isTfaEnabled: true }, user);
    return { message: 'TFA enabled successfully' };
  }

  async disableTfaForUser({
    email,
    tfaToken,
  }: ManageTfa): Promise<{ message: string }> {
    const user = await this.userService.login(email);
    if (!user) {
      throw new NotFoundException('User not found');
    }

    if (!user.isTfaEnabled || !user.tfaSecret) {
      throw new ForbiddenException('TFA is not enabled for this account');
    }

    const secret = await this.security.decrypt(user.tfaSecret);
    if (!this.verifyTfaCode(secret, tfaToken)) {
      throw new BadRequestException('Invalid TFA token');
    }

    await this.userService.updateProfile(
      {
        isTfaEnabled: false,
        tfaSecret: undefined,
      },
      user,
    );

    return { message: 'TFA Disabled successfully' };
  }
}
