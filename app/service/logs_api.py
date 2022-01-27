from app.foo.auditd.loginlogs import LoginLogs, CommandLogs, CzLogs
from app.tools.at import ogs_auth_token


@ogs_auth_token
def acc_login_logs():
    orange = LoginLogs()
    return orange.get_login_logs()


@ogs_auth_token
def acc_login_date():
    orange = LoginLogs()
    return orange.get_date_logs()


@ogs_auth_token
def acc_login_select():
    orange = LoginLogs()
    return orange.get_select_logs()


@ogs_auth_token
def server_com_logs():
    orange = CommandLogs()
    return orange.get_com_logs()


@ogs_auth_token
def server_com_date():
    orange = CommandLogs()
    return orange.get_date_logs()


@ogs_auth_token
def server_com_select():
    orange = CommandLogs()
    return orange.get_select_logs()


@ogs_auth_token
def server_cz_logs():
    orange = CzLogs()
    return orange.get_cz_logs()


@ogs_auth_token
def server_cz_date():
    orange = CzLogs()
    return orange.get_date_logs()


@ogs_auth_token
def server_cz_select():
    orange = CzLogs()
    return orange.get_select_logs()
