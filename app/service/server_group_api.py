from app.foo.property.ServerGroup import AccGroupList, AccGroupAdd, AccGroupUpdate, AccGroupDel


def host_group_list():
    orange = AccGroupList()
    return orange.group_list


def host_group_name_list():
    orange = AccGroupList()
    return orange.group_name_list


def host_group_list_all():
    orange = AccGroupList()
    return orange.group_list_all


def host_group_add():
    orange = AccGroupAdd()
    return orange.host_add


def host_group_update():
    orange = AccGroupUpdate()
    return orange.update


def host_group_del():
    orange = AccGroupDel()
    return orange.host_del
