from app.foo.user.user import AccUserList, AccUserAdd, AccUserUpdate, AccUserDel
from app.tools.at import ogs_auth_token


@ogs_auth_token
def acc_user_list():
    orange = AccUserList()
    return orange.acc_user_list


@ogs_auth_token
def acc_user_auth_list():
    orange = AccUserList()
    return orange.acc_user_auth_list


@ogs_auth_token
def acc_user_list_all():
    orange = AccUserList()
    return orange.acc_user_list_all


@ogs_auth_token
def acc_user_add():
    orange = AccUserAdd()
    return orange.host_add


@ogs_auth_token
def acc_user_update():
    orange = AccUserUpdate()
    return orange.update


@ogs_auth_token
def acc_user_del():
    orange = AccUserDel()
    return orange.host_del


@ogs_auth_token
def acc_user_alias():
    orange = AccUserList()
    return orange.acc_user_alias
