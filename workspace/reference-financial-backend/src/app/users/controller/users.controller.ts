import { AuthUser } from '@app/common';
import { Abilities, SessionUser } from '@app/decorators';
import {
  Body,
  Controller,
  Delete,
  Get,
  Param,
  Post,
  Query,
  UnauthorizedException,
} from '@nestjs/common';
import {
  ApiBearerAuth,
  ApiBody,
  ApiOperation,
  ApiParam,
  ApiResponse,
  ApiTags,
} from '@nestjs/swagger';
import { ChangePasswordDto, DashboardFilter } from '../dto/change-password.dto';
import { RemoveUser } from '../dto/toggle-role.dto';
import {
  ChangePin,
  CreateUser,
  CTP,
  FindManyUser,
  FindOneUser,
  UpdateProfile,
} from '../dto/top-up.dto';
import { Role } from '../interface';
import { AdminService, UsersService } from '../service';

@ApiTags('Users')
@ApiBearerAuth()
@Controller('users')
export class UsersController {
  constructor(
    private readonly users: UsersService,
    private readonly adminService: AdminService,
  ) {}

  @Get('me')
  @ApiOperation({ summary: 'Current user basic JWT payload' })
  @ApiResponse({ status: 200, description: 'Decoded JWT payload' })
  me(@SessionUser() user: AuthUser) {
    return user;
  }

  @Post('create-admins')
  @Abilities('MANAGE_USER')
  @ApiBody({ type: CreateUser })
  @ApiOperation({ summary: 'create new admins' })
  CreateAdmin(@Body() body: CreateUser, @SessionUser() user: AuthUser) {
    if (user.role !== Role.superAdmin || user.roleLevel !== 4) {
      throw new UnauthorizedException('Insufficient accessibility');
    }
    return this.users.createAdmin(body);
  }

  @Get('get-users')
  // @Abilities('MANAGE_USER')
  @ApiOperation({ summary: 'Find Many User' })
  async FindManyUser(@Query() query: FindManyUser) {
    return this.users.findMany(query);
  }

  @Get('get-user')
  // @Abilities('MANAGE_USER')
  @ApiOperation({ summary: 'Find One User' })
  async FindOneUser(@Query() query: FindOneUser) {
    return this.users.findOne(query);
  }

  @Post('transaction-pin')
  @ApiBody({ type: CTP })
  async createTransactionPin(@Body() body: CTP, @SessionUser() user: AuthUser) {
    return this.users.createTransactionPin(body, user);
  }

  @Post('change-transaction-pin')
  @ApiBody({ type: ChangePin })
  async ChangeTransactionPin(
    @Body() body: ChangePin,
    @SessionUser() user: AuthUser,
  ) {
    return this.users.changeTransactionPin(body, user);
  }

  @Post('change-password')
  @ApiOperation({ summary: 'Change password for authenticated user' })
  @ApiResponse({ status: 200, description: 'Password changed successfully' })
  @ApiResponse({ status: 400, description: 'Current password is incorrect' })
  @ApiResponse({ status: 401, description: 'Unauthorized' })
  @ApiResponse({ status: 404, description: 'User not found' })
  async changePassword(
    @SessionUser() user: AuthUser,
    @Body() dto: ChangePasswordDto,
  ) {
    if (!user) throw new UnauthorizedException();
    return this.users.changePassword(dto);
  }

  @Post('update-profile')
  @ApiOperation({ summary: 'Update user profile' })
  @ApiBody({ type: UpdateProfile })
  async updateProfile(
    @Body() data: UpdateProfile,
    @SessionUser() user: AuthUser,
  ) {
    return this.users.updateProfile(data, user);
  }

  @Delete('delete-user/:id')
  @ApiOperation({ summary: 'Delete user by admin' })
  @Abilities('MANAGE_USER')
  @ApiParam({ type: String, required: true, name: 'id' })
  async deleteUser(@Param() param: RemoveUser, @SessionUser() user: AuthUser) {
    if (user.role !== Role.superAdmin || user.roleLevel !== 4) {
      throw new UnauthorizedException('Insufficient accessibility');
    }
    return this.users.deleteUser(param.id);
  }

  @Get('dashboard-chart')
  @Abilities('MANAGE_USER')
  @ApiOperation({ summary: 'Dashboard chart Admin and super admin' })
  async dashboardChart(@Query() query: DashboardFilter) {
    return this.adminService.dashboardChart(query);
  }

  @Get('dashboard-stats')
  @Abilities('MANAGE_USER')
  @ApiOperation({ summary: 'Dashboard stats Admin and super admin' })
  async dashboardStats() {
    return this.adminService.dashboardStats();
  }
}
