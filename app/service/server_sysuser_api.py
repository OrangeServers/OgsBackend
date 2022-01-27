from app.foo.property.SysUser import SysUserList, SysUserAdd, SysUserUpdate, SysUserDel
from app.tools.at import ogs_auth_token


@ogs_auth_token
def sys_user_list():
    orange = SysUserList()
    return orange.sys_user_list


@ogs_auth_token
def sys_name_list():
    orange = SysUserList()
    return orange.sys_user_name_list


@ogs_auth_token
def sys_user_list_all():
    orange = SysUserList()
    return orange.sys_user_list_all


@ogs_auth_token
def sys_user_add():
    orange = SysUserAdd()
    return orange.host_add


@ogs_auth_token
def sys_user_update():
    orange = SysUserUpdate()
    return orange.update


@ogs_auth_token
def sys_user_del():
    orange = SysUserDel()
    return orange.host_del
