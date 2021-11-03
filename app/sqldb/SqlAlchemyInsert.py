from app.sqldb.SqlAlchemySettings import db
from app.sqldb.SqlAlchemyDB import t_host, t_group, t_acc_user, t_sys_user, t_acc_group, t_login_log, t_auth_host, \
    t_command_log, t_line_chart, t_cz_log, t_cron, t_settings


class HostSqlalh:
    def __init__(self):
        pass

    @staticmethod
    def ins_sql(alias, host_ip, host_port, group):
        sql = t_host(alias=alias, host_ip=host_ip, host_port=host_port,
                     group=group)
        db.session.add(sql)
        db.session.commit()
        # db.session.close()


class GroupSqlalh:
    def __init__(self):
        pass

    @staticmethod
    def ins_sql(name, remarks):
        sql = t_group(name=name, nums=0, remarks=remarks)
        db.session.add(sql)
        db.session.commit()


class AccGroupSqlalh:
    def __init__(self):
        pass

    @staticmethod
    def ins_sql(name, remarks):
        sql = t_acc_group(name=name, nums=0, remarks=remarks)
        db.session.add(sql)
        db.session.commit()


class SysUserSqlalh:
    def __init__(self):
        pass

    @staticmethod
    def ins_sql(alias, host_user, host_password, host_key, agreement, remarks):
        sql = t_sys_user(alias=alias, host_user=host_user, host_password=host_password, host_key=host_key,
                         agreement=agreement, nums=0,
                         remarks=remarks)
        db.session.add(sql)
        db.session.commit()


class AccUserSqlalh:
    def __init__(self):
        pass

    @staticmethod
    def ins_sql(alias, name, password, usrole, mail, group, remarks):
        sql = t_acc_user(alias=alias, name=name, password=password, usrole=usrole, mail=mail,
                         group=group, remarks=remarks)
        db.session.add(sql)
        db.session.commit()


class LoginLogSqlalh:
    def __init__(self):
        pass

    @staticmethod
    def ins_sql(login_name, login_nw_ip, login_gw_ip, login_gw_cs, login_agent, login_status, login_reason, login_time):
        sql = t_login_log(login_name=login_name, login_nw_ip=login_nw_ip, login_gw_ip=login_gw_ip,
                          login_gw_cs=login_gw_cs,
                          login_agent=login_agent, login_status=login_status, login_reason=login_reason,
                          login_time=login_time)
        db.session.add(sql)
        db.session.commit()


class CommandLogSqlalh:
    def __init__(self):
        pass

    @staticmethod
    def ins_sql(com_name, com_type, com_info, com_host, com_status, com_reason, com_time):
        sql = t_command_log(com_name=com_name, com_type=com_type, com_info=com_info, com_host=com_host,
                            com_status=com_status,
                            com_reason=com_reason, com_time=com_time)
        db.session.add(sql)
        db.session.commit()


class CzLogSqlalh:
    def __init__(self):
        pass

    @staticmethod
    def ins_sql(cz_name, cz_type, cz_info, cz_details, cz_status, cz_reason, cz_time):
        sql = t_cz_log(cz_name=cz_name, cz_type=cz_type, cz_info=cz_info, cz_details=cz_details,
                       cz_status=cz_status,
                       cz_reason=cz_reason, cz_time=cz_time)
        db.session.add(sql)
        db.session.commit()
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()


class AuthHostSqlalh:
    def __init__(self):
        pass

    @staticmethod
    def ins_sql(name, user, user_group, host_group, sys_user, remarks):
        sql = t_auth_host(name=name, user=user, user_group=user_group, host_group=host_group, sys_user=sys_user,
                          remarks=remarks)
        db.session.add(sql)
        db.session.commit()


class LineChartSqlalh:
    def __init__(self):
        pass

    @staticmethod
    def ins_sql(login_count, user_count, chart_date):
        sql = t_line_chart(login_count=login_count, user_count=user_count, chart_date=chart_date)
        db.session.add(sql)
        db.session.commit()


class CronSqlalh:
    def __init__(self):
        pass

    @staticmethod
    def ins_sql(job_name, job_minute, job_hour, job_day, job_month, job_week, job_hosts, job_groups, job_command,
                job_status, job_remarks=None):
        sql = t_cron(job_name=job_name, job_minute=job_minute, job_hour=job_hour, job_day=job_day,
                     job_month=job_month, job_week=job_week, job_hosts=job_hosts, job_groups=job_groups,
                     job_command=job_command,
                     job_status=job_status, job_remarks=job_remarks)
        db.session.add(sql)
        db.session.commit()


class SettingsSqlalh:
    def __init__(self):
        pass

    @staticmethod
    def ins_sql(name, login_time, register_status, color_matching):
        sql = t_settings(name=name, login_time=login_time, register_status=register_status,
                         color_matching=color_matching)
        db.session.add(sql)
        db.session.commit()
