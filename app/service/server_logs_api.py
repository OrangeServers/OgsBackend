from app.foo.property.ServerManagement import CommandLogs


def server_com_logs():
    orange = CommandLogs()
    return orange.get_com_logs()


def server_com_date():
    orange = CommandLogs()
    return orange.get_date_logs()


def server_com_select():
    orange = CommandLogs()
    return orange.get_select_logs()