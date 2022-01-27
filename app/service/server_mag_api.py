from app.foo.property.ServerManagement import ServerAdd, ServerList, ServerCmd, ServerListCmd, ServerDel, GroupCmd, \
    GroupList, ServerUpdate, ServerScript
from app.tools.at import ogs_auth_token


@ogs_auth_token
def server_add():
    orange = ServerAdd()
    return orange.host_add


@ogs_auth_token
def server_update():
    orange = ServerUpdate()
    return orange.update


@ogs_auth_token
def server_del():
    orange = ServerDel()
    return orange.host_del


@ogs_auth_token
def server_cmd():
    orange = ServerCmd()
    return orange.sh_cmd


@ogs_auth_token
def host_list_all():
    orange = ServerList()
    return orange.server_list_all


@ogs_auth_token
def host_list():
    orange = ServerList()
    return orange.server_list


@ogs_auth_token
def host_list_page():
    orange = ServerList()
    return orange.server_list_page


@ogs_auth_token
def group_list():
    orange = GroupList()
    return orange.server_list


@ogs_auth_token
def server_list_cmd():
    orange = ServerListCmd()
    return orange.sh_list_cmd


@ogs_auth_token
def server_file():
    orange = ServerScript()
    return orange.sh_script()


@ogs_auth_token
def group_cmd():
    orange = GroupCmd()
    return orange.sh_cmd
