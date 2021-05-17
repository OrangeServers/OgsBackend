from app.foo.auth.AuthHost import AuthHostList, AuthHostDel, AuthHostAdd, AuthHostUpdate


def auth_host_list_all():
    orange = AuthHostList()
    return orange.auth_host_list_all


def auth_host_del():
    orange = AuthHostDel()
    return orange.auth_host_del


def auth_group_uplist():
    orange = AuthHostList()
    return orange.test_auth_group


def auth_create_get_list():
    orange = AuthHostList()
    return orange.create_auth_list


def auth_host_add():
    orange = AuthHostAdd()
    return orange.auth_host_add


def auth_host_update():
    orange = AuthHostUpdate()
    return orange.auth_host_update
