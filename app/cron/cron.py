from flask import request, jsonify
from app.cron.CronSettings import scheduler, app
from app.sqldb.SqlAlchemyDB import t_host, t_auth_host, t_sys_user, t_cron, db
from app.sqldb.SqlAlchemyInsert import CronSqlalh
from app.tools.basesec import BaseSec
from app.tools.shellcmd import RemoteConnection, RemoteConnectionKey
from app.tools.SqlListTool import ListTool
from app.tools.at import Log

scheduler.start()


def cron_list_cmd(job_name, job_sys_user, host_id: list, command: str):
    basesec = BaseSec()
    msg_list = []
    alias_list = []
    error_list = []
    sys_user_info = t_sys_user.query.filter_by(alias=job_sys_user).first()
    for hid in host_id:
        host = t_host.query.filter_by(id=hid).first()
        try:
            if sys_user_info.host_key:
                conn = RemoteConnectionKey(host.host_ip, host.host_port, sys_user_info.host_user,
                                           sys_user_info.host_key)
            else:
                password_de = basesec.base_de(sys_user_info.host_password)
                conn = RemoteConnection(host.host_ip, host.host_port, host.host_user,
                                        password_de)
            msg = conn.ssh_cmd(command)
            msg_list.append(msg)
            alias_list.append(host.alias)
        except IOError:
            error_list.append(host.alias)
    if len(error_list) == 0:
        Log.logger.info('job %s cron run.... [ run_msg=%s run_ip%s ]' % (job_name, msg_list, alias_list))
    else:
        Log.logger.info('job %s cron run.... [ run_msg=%s err_ip%s ]' % (job_name, error_list, alias_list))


class OgsCron:
    def __init__(self):
        self.job_name = request.values.get('job_name', default=None)
        self.lt = ListTool()
        self.cron_ins = CronSqlalh()

    # 动态添加定时任务  对现有项目定制。。。。。
    def add_job(self):
        job_minute = request.values.get('job_minute', default="*")
        job_hour = request.values.get('job_hour', default="*")
        job_day = request.values.get('job_day', default="*")
        job_month = request.values.get('job_month', default="*")
        job_week = request.values.get('job_week', default="*")
        job_hosts = request.values.get('job_hosts', default=None)
        job_groups = request.values.get('job_groups')
        job_sys_user = request.values.get('job_sys_user')
        job_command = request.values.get('job_command')
        job_remarks = request.values.get('job_remarks', default=None)
        try:
            job_name_query = t_cron.query.filter_by(job_name=self.job_name).with_hint(t_cron, "force index(job_name)",
                                                                                      'mysql').first()
            if job_name_query is None:
                print(job_sys_user)
                id_list = []
                id_list2 = []
                id_list_rep = ''
                for i in job_groups.split(','):
                    host_list = self.lt.list_gather(
                        t_host.query.filter_by(group=i).with_entities(t_host.id).all())
                    id_list.append(host_list)
                if job_hosts is None or job_hosts == '':
                    id_list_rep = list(set(self.lt.list_gather(id_list)))
                else:
                    for x in job_hosts.split(','):
                        host_list2 = t_host.query.filter_by(alias=x).with_entities(t_host.id).first()
                        id_list2.append(host_list2)
                        id_list_rep = list(set(self.lt.list_gather(id_list) + self.lt.list_gather(id_list2)))
                scheduler.add_job(cron_list_cmd, 'cron', week=job_week, month=job_month, day=job_day, hour=job_hour,
                                  minute=job_minute, args=[self.job_name, job_sys_user, id_list_rep, job_command],
                                  id=self.job_name)
                self.cron_ins.ins_sql(self.job_name, job_minute, job_hour, job_day, job_month, job_week, job_hosts,
                                      job_groups, job_sys_user,
                                      job_command, '启动', job_remarks)
                return jsonify({'cron_add_status': 'true'})
            else:
                return jsonify({'cron_add_status': 'sel_fail'})
        except IOError:
            return jsonify({'cron_add_status': 'con_fail'})
        except Exception as e:
            print(e)
            return jsonify({'cron_add_status': 'fail'})

    # 动态暂停定时任务
    def pause_job(self, job_name=None):
        try:
            if job_name is None:
                job_name = self.job_name
            scheduler.pause_job(job_name)
            t_cron.query.filter_by(job_name=job_name).with_hint(t_cron, "force index(job_name)", 'mysql').update(
                {'job_status': '暂停'})
            db.session.commit()
            return jsonify({'cron_pause_status': 'true'})
        except Exception:
            return jsonify({'cron_pause_status': 'fail'})

    # 动态恢复定时任务
    def resume_job(self, job_name=None):
        try:
            if job_name is None:
                job_name = self.job_name
            scheduler.resume_job(job_name)
            t_cron.query.filter_by(job_name=job_name).with_hint(t_cron, "force index(job_name)", 'mysql').update(
                {'job_status': '启动'})
            db.session.commit()
            return jsonify({'cron_resume_status': 'true'})
        except Exception:
            return jsonify({'cron_resume_status': 'fail'})

    # 动态删除定时任务
    def remove_job(self, job_name=None):
        try:
            if job_name is None:
                job_name = self.job_name
            scheduler.remove_job(job_name)
            job = t_cron.query.filter_by(job_name=job_name).with_hint(t_cron, "force index(job_name)",
                                                                      'mysql').first()
            db.session.delete(job)
            db.session.commit()
            return jsonify({'cron_del_status': 'true'})
        except Exception as e:
            print(e)
            return jsonify({'cron_del_status': 'fail'})

    def com_list_job(self):
        job_name_list = request.values.getlist('job_name_list')
        job_type = request.values.get('job_type')
        try:
            if job_type == 'del':
                for i in job_name_list:
                    self.remove_job(i)
            elif job_type == 'pause':
                for i in job_name_list:
                    self.pause_job(i)
            elif job_type == 'resume':
                for i in job_name_list:
                    self.resume_job(i)
            return jsonify({'cron_com_status': 'true'})
        except Exception as e:
            print(e)
            return jsonify({'cron_com_status': 'fail'})

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
        self.table_page = request.values.get('page', default=1)
        self.table_limit = request.values.get('limit', default=10)
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
            len_msg = t_cron.query.count()
            return jsonify({"host_status": 0,
                            "cron_list_msg": list_msg,
                            "msg": "",
                            "cron_len_msg": len_msg})
        except IOError:
            return jsonify({"cron_list_msg": 'select list msg error',
                            "cron_len_msg": 0})

    @property
    def cron_auth_list(self):
        auth_name = request.values.get('name')
        req_type = request.values.get("req_type")
        auth_list = []
        try:
            user_role_query = t_auth_host.query.filter(t_auth_host.user.like("%{}%".format(auth_name))).all()
            user_role = self.lt.auth_ls_list_que(user_role_query)
            if req_type == 'cron_hosts':
                for i in user_role:
                    query_msg = self.lt.list_gather(t_host.query.filter_by(group=i).with_entities(t_host.alias).all())
                    for y in query_msg:
                        auth_list.append({'name': y, 'value': y})
                return jsonify({'msg': auth_list})
            elif req_type == 'cron_groups':
                for i in user_role:
                    auth_list.append({'name': i, 'value': i})
                return jsonify({'msg': auth_list})
        except IOError:
            return jsonify({'msg': 'fail'})
