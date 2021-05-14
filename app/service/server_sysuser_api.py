from app.foo.property.SysUser import SysUserList, SysUserAdd, SysUserUpdate, SysUserDel


def sys_user_list():
    orange = SysUserList()
    return orange.sys_user_list


def sys_user_list_all():
    orange = SysUserList()
    return orange.sys_user_list_all


def sys_user_add():
    orange = SysUserAdd()
    return orange.host_add


def sys_user_update():
    orange = SysUserUpdate()
    return orange.update


def sys_user_del():
    orange = SysUserDel()
    return orange.host_del
