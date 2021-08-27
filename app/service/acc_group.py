from app.foo.user.group import AccGroupList, AccGroupAdd, AccGroupUpdate, AccGroupDel


def acc_group_list():
    orange = AccGroupList()
    return orange.group_list


def acc_group_name_list():
    orange = AccGroupList()
    return orange.group_name_list


def acc_group_list_all():
    orange = AccGroupList()
    return orange.group_list_all


def acc_group_add():
    orange = AccGroupAdd()
    return orange.host_add


def acc_group_update():
    orange = AccGroupUpdate()
    return orange.update


def acc_group_del():
    orange = AccGroupDel()
    return orange.host_del
