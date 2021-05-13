from app.sqldb.SqlAlchemyDB import Host, t_group, t_acc_user, t_sys_user, t_login_date, t_auth_host, db


class HostSqlalh:
    def __init__(self):
        pass

    @staticmethod
    # def ins_sql(alias, host_ip, host_port, host_user, host_password, group=None):
    def ins_sql(alias, host_ip, host_port, host_user, host_password, group):
        sql = Host(alias=alias, host_ip=host_ip, host_port=host_port, host_user=host_user, host_password=host_password,
                   group=group)
        db.session.add(sql)
        db.session.commit()


class GroupSqlalh:
    def __init__(self):
        pass

    @staticmethod
    def ins_sql(name, remarks):
        sql = t_group(name=name, nums=0, remarks=remarks)
        db.session.add(sql)
        db.session.commit()


class SysUserSqlalh:
    def __init__(self):
        pass

    @staticmethod
    def ins_sql(alias, host_user, host_password, agreement, remarks):
        sql = t_sys_user(alias=alias, host_user=host_user, host_password=host_password, agreement=agreement, nums=0,
                         remarks=remarks)
        db.session.add(sql)
        db.session.commit()


class AccUserSqlalh:
    def __init__(self):
        pass

    @staticmethod
    def ins_sql(alias, name, password, usrole, mail, remarks):
        sql = t_acc_user(alias=alias, name=name, password=password, usrole=usrole, mail=mail,
                         remarks=remarks)
        db.session.add(sql)
        db.session.commit()


class LoginDateSqlalh:
    def __init__(self):
        pass

    @staticmethod
    def ins_sql(login_name, login_nw_ip, login_gw_ip, login_gw_cs, login_agent, login_status, login_reason, login_time):
        sql = t_login_date(login_name=login_name, login_nw_ip=login_nw_ip, login_gw_ip=login_gw_ip, login_gw_cs=login_gw_cs,
                           login_agent=login_agent, login_status=login_status, login_reason=login_reason, login_time=login_time)
        db.session.add(sql)
        db.session.commit()


class AuthHostSqlalh:
    def __init__(self):
        pass

    @staticmethod
    def ins_sql(name, user, user_group, host_group, remarks):
        sql = t_auth_host(name=name, user=user, user_group=user_group, host_group=host_group, remarks=remarks)
        db.session.add(sql)
        db.session.commit()