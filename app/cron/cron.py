import time
from flask import request, jsonify
from datetime import datetime, date
from app.cron.CronSettings import scheduler, app
from app.foo.property.ServerManagement import ServerListCmd
from app.sqldb.SqlAlchemyDB import t_host
from app.tools.basesec import BaseSec
from app.tools.shellcmd import RemoteConnection
from app.tools.SqlListTool import ListTool
from app.tools.at import Log


def cron_list_cmd(host_id: list, command: str):
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
        print(msg_list)
    else:
        print(error_list, alias_list)


# def print_test(param):
#     print("姓名：{}".format(param))
#
#
# # 动态启动定时任务
# @app.route('/start')
# def start():
#     # 5.启动调度器，不阻塞
#     scheduler.start()
#     return '启动成功'


class OgsCron:
    def __init__(self):
        self.job_name = request.values.get('job_name', default=None)
        self.lt = ListTool()

    # 动态添加定时任务2  对现有项目定制。。。。。
    def add_job(self):
        job_minute = request.values.get('job_minute', default="*")
        job_hour = request.values.get('job_hour', default="*")
        job_day = request.values.get('job_day', default="*")
        job_month = request.values.get('job_month', default="*")
        job_week = request.values.get('job_week', default="*")
        job_groups = request.values.get('job_groups')
        job_command = request.values.get('job_command')
        job_remarks = request.values.get('job_remarks', default=None)
        host_list = self.lt.list_gather(t_host.query.filter_by(group=job_groups).with_entities(t_host.id).all())
        scheduler.add_job(cron_list_cmd, 'cron', week=job_week, month=job_month, day=job_day, hour=job_hour,
                          minute=job_minute, args=[host_list, job_command],
                          id='1')
        return "动态添加定时任务：{}".format(self.job_name)

    # 动态暂停定时任务
    def pause_job(self):
        scheduler.pause_job(self.job_name)
        return "动态暂停定时任务成功：{}".format(self.job_name)

    # 动态恢复定时任务
    def resume_job(self):
        scheduler.resume_job(self.job_name)
        return "动态恢复定时任务成功：{}".format(self.job_name)

    # 动态删除定时任务
    def remove_job(self):
        scheduler.remove_job(self.job_name)
        return "动态删除定时任务成功：{}".format(self.job_name)

    # 关闭所有定时任务
    @property
    def close_job(self):
        scheduler.shutdown()
        return "关闭所有定时任务成功"


# 动态添加定时任务
@app.route("/add_job/<param>")
def add_job(param):
    cron_list_cmd([1], 'date')
    # scheduler.add_job(print_test, 'interval', seconds=3, args=[param], id=param)
    # def cm1():
    #     with app.app_context():
    #         msg = cron_list_cmd([1], 'date')
    #         return msg
    scheduler.add_job(cron_list_cmd, 'interval', seconds=3, args=[[1], 'hostname && date'], id=param)
    # msg = x1.sh_list_cmd
    return "动态添加定时任务：{}".format(param)


if __name__ == '__main__':
    print('cron')
    # app.run(host='0.0.0.0', port=28110)
    # aps_run()
