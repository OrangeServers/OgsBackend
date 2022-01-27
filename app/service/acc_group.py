from app.foo.user.group import AccGroupList, AccGroupAdd, AccGroupUpdate, AccGroupDel
from app.tools.at import ogs_auth_token


@ogs_auth_token
def acc_group_list():
    orange = AccGroupList()
    return orange.group_list


@ogs_auth_token
def acc_group_name_list():
    orange = AccGroupList()
    return orange.group_name_list


@ogs_auth_token
def acc_group_list_all():
    orange = AccGroupList()
    return orange.group_list_all


@ogs_auth_token
def acc_group_add():
    orange = AccGroupAdd()
    return orange.host_add


@ogs_auth_token
def acc_group_update():
    orange = AccGroupUpdate()
    return orange.update


@ogs_auth_token
def acc_group_del():
    orange = AccGroupDel()
    return orange.host_del
