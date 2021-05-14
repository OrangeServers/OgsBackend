from app.foo.property.ServerManagement import ServerAdd, ServerList, ServerCmd2, ServerListCmd, ServerDel, GroupCmd, \
    GroupList, ServerUpdate, ServerScript


def server_add():
    orange = ServerAdd()
    return orange.host_add


def server_update():
    orange = ServerUpdate()
    return orange.update


def server_del():
    orange = ServerDel()
    return orange.host_del


def server_cmd():
    orange = ServerCmd2()
    return orange.sh_cmd


def host_list_all():
    orange = ServerList()
    return orange.server_list_all


def host_list():
    orange = ServerList()
    return orange.server_list


def host_list_page():
    orange = ServerList()
    return orange.server_list_page


def group_list():
    orange = GroupList()
    return orange.server_list


def server_list_cmd():
    orange = ServerListCmd()
    return orange.sh_list_cmd


def server_file():
    orange = ServerScript()
    return orange.sh_script()


def group_cmd():
    orange = GroupCmd()
    return orange.sh_cmd
