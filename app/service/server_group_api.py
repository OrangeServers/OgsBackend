from app.foo.property.ServerGroup import ServerGroupList, ServerGroupAdd, ServerGroupUpdate, ServerGroupDel


def host_group_list():
    orange = ServerGroupList()
    return orange.group_list


def host_group_name_list():
    orange = ServerGroupList()
    return orange.group_name_list


def host_group_list_all():
    orange = ServerGroupList()
    return orange.group_list_all


def host_group_add():
    orange = ServerGroupAdd()
    return orange.host_add


def host_group_update():
    orange = ServerGroupUpdate()
    return orange.update


def host_group_del():
    orange = ServerGroupDel()
    return orange.host_del
