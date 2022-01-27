from app.foo.auth.AuthHost import AuthHostList, AuthHostDel, AuthHostAdd, AuthHostUpdate
from app.tools.at import ogs_auth_token


@ogs_auth_token
def auth_host_list_all():
    orange = AuthHostList()
    return orange.auth_host_list_all


@ogs_auth_token
def auth_group_uplist():
    orange = AuthHostList()
    return orange.auth_group_role


@ogs_auth_token
def auth_create_get_list():
    orange = AuthHostList()
    return orange.create_auth_list


@ogs_auth_token
def auth_host_add():
    orange = AuthHostAdd()
    return orange.auth_host_add


@ogs_auth_token
def auth_host_update():
    orange = AuthHostUpdate()
    return orange.auth_host_update


@ogs_auth_token
def auth_host_del():
    orange = AuthHostDel()
    return orange.auth_host_del
