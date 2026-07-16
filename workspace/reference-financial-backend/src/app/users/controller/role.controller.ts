import { AuthUser, CAPABILITIES } from '@app/common';
import { Abilities, SessionUser } from '@app/decorators';
import {
  Body,
  Controller,
  Get,
  Patch,
  Post,
  Query,
  UnauthorizedException,
} from '@nestjs/common';
import { ApiBearerAuth, ApiOperation, ApiTags } from '@nestjs/swagger';
import { AssignRole, ChangeUserRoleDto } from '../dto/toggle-role.dto';
import { FindManyUser, FindOneUser } from '../dto/top-up.dto';
import { Role } from '../interface';
import { RoleService } from '../service';

@ApiTags('Users')
@ApiBearerAuth()
@Controller('users')
export class RoleController {
  constructor(private readonly roleService: RoleService) {}

  @Get('manage-user')
  @ApiOperation({ summary: 'manage user' })
  @Abilities('MANAGE_USER')
  ManageUser(@Query() query: FindManyUser, @SessionUser() user: AuthUser) {
    if (user.role !== Role.superAdmin || user.roleLevel !== 4) {
      throw new UnauthorizedException('Insufficient accessibility');
    }

    const allowedRoles = [
      Role.pro,
      Role.superAdmin,
      Role.publish,
      Role.admin,
      Role.marketer,
    ];

    return this.roleService.getRoleWithDetails({
      ...query,
      // type: [userType.internal],
      roleName: allowedRoles,
      include: ['privileges', 'roles'],
    });
  }

  @Get('single-user-with-role')
  @Abilities('MANAGE_USER')
  @ApiOperation({ summary: 'Single user with role and permission details' })
  SingleUserWithRole(
    @Query() param: FindOneUser,
    @SessionUser() user: AuthUser,
  ) {
    if (user.role !== Role.superAdmin || user.roleLevel !== 4) {
      throw new UnauthorizedException('Insufficient accessibility');
    }
    return this.roleService.getSingleUserWithRoleAndPermission(param);
  }

  @Post('give-access')
  @Abilities('MANAGE_USER')
  @ApiOperation({ summary: 'Assign access to role' })
  AssignPermission(@Body() body: AssignRole, @SessionUser() user: AuthUser) {
    if (user.role !== Role.superAdmin || user.roleLevel !== 4) {
      throw new UnauthorizedException('Insufficient accessibility');
    }
    return this.roleService.assignPermission(body);
  }

  @Post('remove-access')
  @Abilities('MANAGE_USER')
  @ApiOperation({ summary: 'Remove access from role' })
  RemoveAccess(@Body() body: AssignRole, @SessionUser() user: AuthUser) {
    if (user.role !== Role.superAdmin || user.roleLevel !== 4) {
      throw new UnauthorizedException('Insufficient accessibility');
    }
    return this.roleService.removeAccess(body);
  }

  @Get('available-access')
  @Abilities('MANAGE_USER')
  @ApiOperation({ summary: 'Available access to give to roles' })
  AvailableAccess(@SessionUser() user: AuthUser) {
    if (user.role !== Role.superAdmin || user.roleLevel !== 4) {
      throw new UnauthorizedException('Insufficient accessibility');
    }
    return CAPABILITIES;
  }

  @Patch('edit-user-role')
  @Abilities('MANAGE_USER')
  @ApiOperation({ summary: 'Edit user role' })
  EditUserRole(@Body() body: ChangeUserRoleDto, @SessionUser() user: AuthUser) {
    if (user.role !== Role.superAdmin || user.roleLevel !== 4) {
      throw new UnauthorizedException('Insufficient accessibility');
    }
    return this.roleService.changeUserRole(body);
  }
}
