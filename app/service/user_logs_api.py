from app.foo.user.user import LoginLogs


def acc_login_logs():
    orange = LoginLogs()
    return orange.get_login_logs()


def acc_login_date():
    orange = LoginLogs()
    return orange.get_date_logs()


def acc_login_select():
    orange = LoginLogs()
    return orange.get_select_logs()