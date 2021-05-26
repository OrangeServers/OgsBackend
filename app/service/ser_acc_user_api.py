from app.foo.user.user import AccUserList, AccUserAdd, AccUserUpdate, AccUserDel


def acc_user_list():
    orange = AccUserList()
    return orange.sys_user_list


def acc_user_auth_list():
    orange = AccUserList()
    return orange.sys_user_auth_list


def acc_user_list_all():
    orange = AccUserList()
    return orange.sys_user_list_all


def acc_user_add():
    orange = AccUserAdd()
    return orange.host_add


def acc_user_update():
    orange = AccUserUpdate()
    return orange.update


def acc_user_del():
    orange = AccUserDel()
    return orange.host_del