from app.foo.auditd.loginlogs import LoginLogs, CommandLogs, CzLogs


def acc_login_logs():
    orange = LoginLogs()
    return orange.get_login_logs()


def acc_login_date():
    orange = LoginLogs()
    return orange.get_date_logs()


def acc_login_select():
    orange = LoginLogs()
    return orange.get_select_logs()


def server_com_logs():
    orange = CommandLogs()
    return orange.get_com_logs()


def server_com_date():
    orange = CommandLogs()
    return orange.get_date_logs()


def server_com_select():
    orange = CommandLogs()
    return orange.get_select_logs()


def server_cz_logs():
    orange = CzLogs()
    return orange.get_cz_logs()


def server_cz_date():
    orange = CzLogs()
    return orange.get_date_logs()


def server_cz_select():
    orange = CzLogs()
    return orange.get_select_logs()
