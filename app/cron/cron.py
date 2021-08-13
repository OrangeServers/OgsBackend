from flask import request, jsonify
from app.cron.CronSettings import scheduler, app
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
        try:
            job_name_query = t_cron.query.filter_by(job_name=self.job_name).with_hint(t_cron,"force index(job_name)", 'mysql').first()
            if job_name_query is None:
                id_list = []
                for i in job_groups.split(','):
                    host_list = self.lt.list_gather(
                        t_host.query.filter_by(group=i).with_hint(t_cron, "force index(job_name)",
                                                                  'mysql').with_entities(t_host.id).all())
                    id_list.append(host_list)
                id_list_rep = self.lt.list_gather(id_list)
                scheduler.add_job(cron_list_cmd, 'cron', week=job_week, month=job_month, day=job_day, hour=job_hour,
                                  minute=job_minute, args=[self.job_name, id_list_rep, job_command],
                                  id=self.job_name)
                self.cron_ins.ins_sql(self.job_name, job_minute, job_hour, job_day, job_month, job_week, job_groups,
                                      job_command, '启动', job_remarks)
                return jsonify({'cron_add_status': 'true'})
            else:
                return jsonify({'cron_add_status': 'sel_fail'})
        except IOError:
            return jsonify({'cron_add_status': 'con_fail'})
        except Exception:
            return jsonify({'cron_add_status': 'fail'})

    # 动态暂停定时任务
    def pause_job(self):
        try:
            scheduler.pause_job(self.job_name)
            t_cron.query.filter_by(job_name=self.job_name).with_hint(t_cron, "force index(job_name)", 'mysql').update(
                {'job_status': '暂停'})
            db.session.commit()
            return jsonify({'cron_pause_status': 'true'})
        except Exception:
            return jsonify({'cron_pause_status': 'fail'})

    # 动态恢复定时任务
    def resume_job(self):
        try:
            scheduler.resume_job(self.job_name)
            t_cron.query.filter_by(job_name=self.job_name).with_hint(t_cron, "force index(job_name)", 'mysql').update(
                {'job_status': '启动'})
            db.session.commit()
            return jsonify({'cron_resume_status': 'true'})
        except Exception:
            return jsonify({'cron_resume_status': 'fail'})

    # 动态删除定时任务
    def remove_job(self):
        try:
            scheduler.remove_job(self.job_name)
            job = t_cron.query.filter_by(job_name=self.job_name).with_hint(t_cron, "force index(job_name)",
                                                                           'mysql').first()
            db.session.delete(job)
            db.session.commit()
            return jsonify({'cron_del_status': 'true'})
        except Exception:
            return jsonify({'cron_del_status': 'fail'})

    # 关闭所有定时任务
    @property
    def close_job(self):
        try:
            scheduler.shutdown()
            return jsonify({'cron_shutdown_status': 'true'})
        except Exception:
            return jsonify({'cron_shutdown_status': 'fail'})


class CronList:
    def __init__(self):
        self.lt = ListTool()
        self.table_page = request.values.get('page')
        self.table_limit = request.values.get('limit')
        self.table_offset = (int(self.table_page) - 1) * 10

    @property
    def cron_list(self):
        try:
            cron_id = request.values.get("id")
            query_msg = t_cron.query.filter_by(id=cron_id).first()
            list_msg = self.lt.dict_reset_pop_auto(query_msg)
            return jsonify(list_msg)
        except IOError:
            return jsonify({"cron_list_msg": 'select list msg error'})

    @property
    def cron_list_all(self):
        try:
            query_msg = t_cron.query.offset(self.table_offset).limit(self.table_limit).all()
            list_msg = self.lt.dict_ls_reset_dict_auto(query_msg)
            len_msg = t_cron.query.offset(self.table_offset).limit(self.table_limit).count()
            return jsonify({"host_status": 0,
                            "cron_list_msg": list_msg,
                            "msg": "",
                            "cron_len_msg": len_msg})
        except IOError:
            return jsonify({"cron_list_msg": 'select list msg error',
                            "cron_len_msg": 0})


if __name__ == '__main__':
    print('cron')
    # app.run(host='0.0.0.0', port=28110)
    # aps_run()
