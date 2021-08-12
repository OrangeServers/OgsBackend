import time
from flask import request, jsonify
from datetime import datetime, date
from app.cron.CronSettings import scheduler, app
from app.foo.property.ServerManagement import ServerListCmd
from app.sqldb.SqlAlchemyDB import t_host, t_cron, db
from app.sqldb.SqlAlchemyInsert import CronSqlalh
from app.tools.basesec import BaseSec
from app.tools.shellcmd import RemoteConnection
from app.tools.SqlListTool import ListTool
from app.tools.at import Log

scheduler.start()


def cron_list_cmd(job_name, host_id: list, command: str):
    basesec = BaseSec()
    msg_list = []
    alias_list = []
    error_list = []
    for hid in host_id:
        host = t_host.query.filter_by(id=hid).first()
        host_dict = host.__dict__
        password_de = basesec.base_de(host_dict['host_password'])
        try:
            conn = RemoteConnection(host_dict['host_ip'], host_dict['host_port'], host_dict['host_user'],
                                    password_de)
            msg = conn.ssh_cmd(command)
            msg_list.append(msg)
            alias_list.append(host_dict['alias'])
        except IOError:
            error_list.append(host_dict['alias'])
    if len(error_list) == 0:
        Log.logger.info('job %s cron run.... [ run_msg=%s run_ip%s ]' % (job_name, msg_list, alias_list))
    else:
        Log.logger.info('job %s cron run.... [ run_msg=%s err_ip%s ]' % (job_name, error_list, alias_list))


class OgsCron:
    def __init__(self):
        self.job_name = request.values.get('job_name')
        self.lt = ListTool()
        self.cron_ins = CronSqlalh()

    # 动态添加定时任务  对现有项目定制。。。。。
    def add_job(self):
        job_minute = request.values.get('job_minute', default="*")
        job_hour = request.values.get('job_hour', default="*")
        job_day = request.values.get('job_day', default="*")
        job_month = request.values.get('job_month', default="*")
        job_week = request.values.get('job_week', default="*")
        job_groups = request.values.get('job_groups')
        job_command = request.values.get('job_command')
        job_remarks = request.values.get('job_remarks', default=None)
        id_list = []
        for i in job_groups.split(','):
            host_list = self.lt.list_gather(t_host.query.filter_by(group=i).with_entities(t_host.id).all())
            id_list.append(host_list)
        id_list_rep = self.lt.list_gather(id_list)
        # host_list = self.lt.list_gather(t_host.query.filter_by(group=job_groups).with_entities(t_host.id).all())
        scheduler.add_job(cron_list_cmd, 'cron', week=job_week, month=job_month, day=job_day, hour=job_hour,
                          minute=job_minute, args=[self.job_name, id_list_rep, job_command],
                          id=self.job_name)
        self.cron_ins.ins_sql(self.job_name, job_minute, job_hour, job_day, job_month, job_week, job_groups,
                              job_command, '启动', job_remarks)
        return "动态添加定时任务：{}".format(self.job_name)

    # 动态暂停定时任务
    def pause_job(self):
        scheduler.pause_job(self.job_name)
        t_cron.query.filter_by(job_name=self.job_name).update({'job_status': '暂停'})
        db.session.commit()
        return "动态暂停定时任务成功：{}".format(self.job_name)

    # 动态恢复定时任务
    def resume_job(self):
        scheduler.resume_job(self.job_name)
        t_cron.query.filter_by(job_name=self.job_name).update({'job_status': '启动'})
        db.session.commit()
        return "动态恢复定时任务成功：{}".format(self.job_name)

    # 动态删除定时任务
    def remove_job(self):
        scheduler.remove_job(self.job_name)
        job = t_cron.query.filter_by(job_name=self.job_name).first()
        db.session.delete(job)
        db.session.commit()
        return "动态删除定时任务成功：{}".format(self.job_name)

    # 关闭所有定时任务
    @property
    def close_job(self):
        scheduler.shutdown()
        return "关闭所有定时任务成功"


if __name__ == '__main__':
    print('cron')
    # app.run(host='0.0.0.0', port=28110)
    # aps_run()
