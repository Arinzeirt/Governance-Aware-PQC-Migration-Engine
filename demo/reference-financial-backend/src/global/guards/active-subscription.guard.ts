import { ACTIVE_SUBSCRIPTION_KEY } from '@app/decorators';
import { SubscriptionStatus } from '@app/subscription/input';
import { SubscriptionService } from '@app/subscription/service';
import {
  CanActivate,
  ExecutionContext,
  ForbiddenException,
  Injectable,
} from '@nestjs/common';
import { Reflector } from '@nestjs/core';

@Injectable()
export class ActiveSubscriptionGuard implements CanActivate {
  constructor(
    private reflector: Reflector,
    private subscriptionService: SubscriptionService,
  ) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const isRequired = this.reflector.getAllAndOverride<boolean>(
      ACTIVE_SUBSCRIPTION_KEY,
      [context.getHandler(), context.getClass()],
    );

    if (!isRequired) {
      return true;
    }

    const { user } = context.switchToHttp().getRequest();

    if (!user) {
      throw new ForbiddenException('User not authenticated');
    }

    const activeSub =
      await this.subscriptionService.getActiveSubscription(user);

    if (!activeSub || activeSub.status !== SubscriptionStatus.active) {
      throw new ForbiddenException(
        'You need an active subscription to access this resource',
      );
    }

    return true;
  }
}
