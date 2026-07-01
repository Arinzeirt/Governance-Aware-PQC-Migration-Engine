/* eslint-disable @typescript-eslint/no-unused-vars */
import { AuthUser, JwtPayload } from '@app/common';
import { IUser, Role } from '@app/users/interface';
import { UsersService } from '@app/users/service';
import {
  BadRequestException,
  ForbiddenException,
  Injectable,
  UnauthorizedException,
} from '@nestjs/common';
import { JsonWebTokenError, JwtService } from '@nestjs/jwt';
import { ResendOtpDto, VerifyOtpDto } from 'src/app/auth/dto/otp.dto';
import { jwtConstants } from './constants';
import {
  ForgotPasswordDto,
  recaptchaResponse,
} from './dto/forgot-password.dto';
import { LoginDto } from './dto/login.dto';
import { PartnerShip, ResetPasswordDto } from './dto/reset-password.dto';
import { SignupDto, Suspend, suspendResponse } from './dto/signup.dto';
import { ReferralService } from '@app/referral/referral.service';
import { SecurityService } from '@app/helpers';
import { TwoFAService } from '@app/users/service/twofa.service';
import { AxiosError } from 'axios';
import { HttpClientService, MailService, template } from '@app/services';
import { ConfigService } from '@nestjs/config';
import { EventEmitter2 } from '@nestjs/event-emitter';
import { validate } from 'deep-email-validator';

const retryCount: Map<string, Suspend> = new Map<string, Suspend>();
@Injectable()
export class AuthService {
  constructor(
    private readonly users: UsersService,
    private readonly jwtService: JwtService,
    private readonly referralService: ReferralService,
    private readonly security: SecurityService,
    private readonly twoFAService: TwoFAService,
    private readonly mailService: MailService,
    private readonly httpService: HttpClientService,
    private readonly configService: ConfigService,
    private readonly eventEmitter: EventEmitter2,
  ) {}

  async register(dto: SignupDto) {
    const res = await validate(dto.email);
    if (!res.valid) throw new ForbiddenException('Invalid email address');

    const existing: IUser | null = await this.users.findByEmail(
      dto.email.toLowerCase(),
    );
    if (existing) {
      if (!existing.isVerified) {
        void this.resendOtp({ email: existing.email, purpose: 'verify' });
        throw new BadRequestException('Account not verified new Otp sent');
      }
      throw new BadRequestException('Email already in use');
    }

    const referDetails: {
      directReferrerId?: string | undefined;
      userId?: string | undefined;
    } = {};

    if (dto.referral) {
      const referral = await this.users.findOne({
        refercode: dto.referral,
      });

      if (!referral.data) {
        throw new ForbiddenException('Incorrect referral code');
      }

      if (!referral.data.isVerified) {
        throw new ForbiddenException('Referrer Account not verified');
      }

      referDetails.directReferrerId = referral.data.id;
    }

    if (dto.username) {
      const { data } = await this.users.findOne({ username: dto.username });
      if (data) throw new ForbiddenException('username already taken');
    }

    const data = await this.users.createUser(dto);
    if (data) referDetails.userId = data.id;
    void this.referralService.create(referDetails);
    return data;
  }

  async verifyEmail(dto: VerifyOtpDto) {
    return this.users.verifyEmail({
      email: dto.email.toLowerCase(),
      otp: dto.otp,
    });
  }

  async resendOtp(dto: ResendOtpDto) {
    return this.users.resendOtp({
      email: dto.email.toLowerCase(),
      purpose: dto.purpose,
    });
  }

  async userLogin(dto: LoginDto) {
    const data = this.suspendUser(dto.email);
    if (data.suspended && data?.suspensionTime) {
      throw new ForbiddenException(
        `Your account has been suspended for 5 Minutes`,
      );
    }

    if (data.suspended && data.indefinite) {
      throw new ForbiddenException(
        'Your account has been suspended. Contact support.',
      );
    }

    const user = await this.users.login(dto.email.toLowerCase());

    if (!user || !(await user.validatePassword(dto.password))) {
      throw new ForbiddenException('Invalid credentials');
    }

    if (!user.isVerified) {
      throw new ForbiddenException('Email not verified');
    }

    if (![Role.follower, Role.pro].includes(user.role)) {
      throw new BadRequestException('Access denied for this role');
    }

    const {
      password,
      createdAt,
      updatedAt,
      tfaSecret,
      transactionPin,
      ...sanitizedUser
    } = user;

    if (user.isTfaEnabled) {
      return {
        status: 'TFA_REQUIRED',
        message: 'Enter your 2FA code',
        email: sanitizedUser,
      };
    }

    const payload = {
      id: user.id,
      email: user.email,
      role: user.role,
      roleLevel: user.roleLevel,
      username: user.username,
    };

    retryCount.delete(dto.email);
    this.eventEmitter.emit('user.activity', user.id);
    const access = await this.generateTokens(payload, '1h');
    const refresh = await this.generateTokens(payload, '2h');
    return {
      streple_auth_token: access,
      streple_refresh_token: refresh,
      token_type: 'Bearer',
      expires_in: jwtConstants.expiresIn,
      data: sanitizedUser,
    };
  }

  async adminLogin(dto: LoginDto) {
    const data = this.suspendUser(dto.email);
    if (data.suspended && data?.suspensionTime) {
      throw new ForbiddenException(
        `Your account has been suspended for 5 Minutes`,
      );
    }

    if (data.suspended && data.indefinite) {
      throw new ForbiddenException(
        'Your account has been suspended. Contact support.',
      );
    }

    const user = await this.users.login(dto.email.toLowerCase());
    // if (data?.suspended && data.isFirst) {
    //   // suspend account
    // }

    if (!user || !(await user.validatePassword(dto.password))) {
      throw new ForbiddenException('Invalid credentials');
    }

    if (!user.isVerified) {
      throw new ForbiddenException('Email not verified');
    }

    if ([Role.follower].includes(user.role)) {
      throw new BadRequestException('Access denied for this role');
    }

    const {
      password,
      createdAt,
      updatedAt,
      tfaSecret,
      transactionPin,
      ...sanitizedUser
    } = user;

    if (user.isTfaEnabled) {
      return {
        status: 'TFA_REQUIRED',
        message: 'Enter your 2FA code',
        data: sanitizedUser,
      };
    }

    const payload = {
      id: user.id,
      email: user.email,
      role: user.role,
      roleLevel: user.roleLevel,
      username: user.username,
    };

    retryCount.delete(dto.email);

    const access = await this.generateTokens(payload, '1h');
    const refresh = await this.generateTokens(payload, '2h');
    return {
      streple_auth_token: access,
      streple_refresh_token: refresh,
      token_type: 'Bearer',
      expires_in: jwtConstants.expiresIn,
      data: sanitizedUser,
    };
  }

  async verifyTfaLogin(email: string, tfaToken: string) {
    const user = await this.users.login(email.toLowerCase());
    if (!user) throw new BadRequestException('Invalid user');

    if (!user.isTfaEnabled || !user.tfaSecret) {
      throw new ForbiddenException('TFA is not enabled for this account');
    }

    const secret = await this.security.decrypt(user.tfaSecret);
    const isValid = await this.twoFAService.verifyTfaCode(secret, tfaToken);

    if (!isValid) {
      throw new BadRequestException('Invalid TFA code');
    }

    const payload = {
      id: user.id,
      email: user.email,
      role: user.role,
      roleLevel: user.roleLevel,
      username: user.username,
    };
    this.eventEmitter.emit('user.activity', user.id);
    const { password, createdAt, updatedAt, tfaSecret, ...sanitizedUser } =
      user;
    const access = await this.generateTokens(payload, '1h');
    const refresh = await this.generateTokens(payload, '2h');
    return {
      streple_auth_token: access,
      streple_refresh_token: refresh,
      token_type: 'Bearer',
      expires_in: jwtConstants.expiresIn,
      data: sanitizedUser,
    };
  }

  async forgotPassword(dto: ForgotPasswordDto) {
    return await this.users.forgotPassword({ email: dto.email.toLowerCase() });
  }

  async verifyOtp(dto: VerifyOtpDto) {
    return this.users.verifyOtp({
      email: dto.email.toLowerCase(),
      otp: dto.otp,
    });
  }

  async resetPassword(dto: ResetPasswordDto) {
    return await this.users.resetPassword({
      email: dto.email.toLowerCase(),
      newPassword: dto.newPassword,
    });
  }

  async recaptchaVerification(token: string) {
    try {
      const response = await this.httpService.post<recaptchaResponse>({
        uri: 'https://www.google.com/recaptcha/api/siteverify',
        body: {
          secret: this.configService.getOrThrow('RECAPTCHA_SECRET_KEY'),
          response: token,
        },
      });

      console.log(response);

      return { message: 'reCAPTCHA verified successfully' };
    } catch (error) {
      if (error instanceof AxiosError) {
        throw new BadRequestException(error.response?.data);
      }
      throw error;
    }
  }

  async refreshToken(token: string) {
    try {
      const payload: JwtPayload = await this.jwtService.verifyAsync(token, {
        secret: jwtConstants.secret,
      });

      if (!payload) {
        throw new UnauthorizedException('Invalid or expired token');
      }

      const { iat, exp, ...rest } = payload;
      const access = await this.generateTokens(rest, '1h');
      const refresh = await this.generateTokens(rest, '2h');

      return { streple_access_token: access, streple_refresh_token: refresh };
    } catch (error) {
      if (error instanceof JsonWebTokenError) {
        throw new BadRequestException(error.message);
      }
      throw error;
    }
  }

  async partnership(payload: PartnerShip) {
    try {
      await Promise.all([
        this.mailService.sendMail(
          'partnership@streple.com',
          template.infoPartner,
          'New Partnership Request – Action Required',
          {},
        ),
        this.mailService.sendMail(
          payload.email,
          template.partnership,
          'Partnership request received',
          {
            email: payload.email,
            fullName: payload.fullName,
            message: payload.message,
          },
        ),
      ]);

      return { message: 'Request receive successfully' };
    } catch (error) {
      if (error instanceof AxiosError) {
        throw new BadRequestException(error.response?.data);
      }
      throw error;
    }
  }

  async support(payload: PartnerShip) {
    try {
      await Promise.all([
        this.mailService.sendMail(
          'support@streple.com',
          template.infoSupport,
          'New Partnership Request – Action Required',
          {},
        ),
        this.mailService.sendMail(
          payload.email,
          template.customer,
          'Partnership request received',
          {
            email: payload.email,
            fullName: payload.fullName,
            message: payload.message,
          },
        ),
      ]);

      return { message: 'Your request has been log successfully' };
    } catch (error) {
      if (error instanceof AxiosError) {
        throw new BadRequestException(error.response?.data);
      }
      throw error;
    }
  }

  private generateTokens(user: AuthUser, expiresIn: '1h' | '2h') {
    return this.jwtService.signAsync<AuthUser>(user, {
      secret: jwtConstants.secret,
      expiresIn: expiresIn,
    });
  }

  private suspendUser(filter: string): suspendResponse {
    const WINDOW_MS = 5 * 60_000;
    const TEMP_THRESHOLD = 5;
    const INDEFINITE_THRESHOLD = 10;
    const now = new Date();
    let entry = retryCount.get(filter);

    if (!entry) {
      entry = {
        use_count: 1,
        total_attempts: 1,
        firstAttempt: now,
        suspendedUntil: null,
        indefinite: false,
      };
      retryCount.set(filter, entry);
      return { suspended: false, indefinite: false };
    }

    // If indefinite suspended already
    if (entry.indefinite) {
      return { suspended: true, indefinite: true };
    }

    // Window duration logic
    const windowEnd = new Date(entry.firstAttempt.getTime() + WINDOW_MS);
    if (now > windowEnd) {
      entry.use_count = 1;
      entry.firstAttempt = now;
      entry.suspendedUntil = null;
      entry.indefinite = false;
      entry.total_attempts = 6;
    } else {
      entry.use_count += 1;
      entry.total_attempts += 1;
    }

    // Check for indefinite suspension
    if (entry.total_attempts >= INDEFINITE_THRESHOLD) {
      entry.indefinite = true;
      retryCount.set(filter, entry);
      return { suspended: true, indefinite: true };
    }

    // Check for temporary suspension
    if (entry.use_count >= TEMP_THRESHOLD) {
      entry.suspendedUntil = new Date(now.getTime() + WINDOW_MS);
      retryCount.set(filter, entry);
      return {
        suspended: true,
        indefinite: false,
        suspensionTime: entry.suspendedUntil,
      };
    }

    retryCount.set(filter, entry);
    console.log(
      `Filter: ${filter}, Attempts: ${entry.use_count}, TotalAttempts: ${entry.total_attempts}, FirstAttempt: ${entry.firstAttempt.toISOString()}`,
    );
    return { suspended: false, indefinite: false };
  }
}
