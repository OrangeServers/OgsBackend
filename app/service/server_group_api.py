from app.foo.property.ServerGroup import ServerGroupList, ServerGroupAdd, ServerGroupUpdate, ServerGroupDel
from app.tools.at import ogs_auth_token


@ogs_auth_token
def host_group_list():
    orange = ServerGroupList()
    return orange.group_list


@ogs_auth_token
def host_group_name_list():
    orange = ServerGroupList()
    return orange.group_name_list


@ogs_auth_token
def host_group_list_all():
    orange = ServerGroupList()
    return orange.group_list_all


@ogs_auth_token
def host_group_add():
    orange = ServerGroupAdd()
    return orange.host_add


@ogs_auth_token
def host_group_update():
    orange = ServerGroupUpdate()
    return orange.update


@ogs_auth_token
def host_group_del():
    orange = ServerGroupDel()
    return orange.host_del
