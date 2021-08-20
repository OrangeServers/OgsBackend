import time
from flask import request, jsonify
from werkzeug.utils import secure_filename
from app.tools.shellcmd import RemoteConnection
from app.foo.local.LocalShell import LocalShell
from app.sqldb.SqlAlchemySettings import db
from app.sqldb.SqlAlchemyDB import t_host, t_group, t_auth_host, t_acc_user, t_cz_log
from app.sqldb.SqlAlchemyInsert import HostSqlalh, CommandLogSqlalh, CzLogSqlalh
from app.tools.SqlListTool import ListTool
from app.tools.basesec import BaseSec


class ServerList:
    def __init__(self):
        self.lt = ListTool()

    @property
    def server_count_all(self):
        try:
            host_len_msg = t_host.query.count()
            user_len_msg = t_acc_user.query.count()
            group_len_msg = t_group.query.count()
            return jsonify({
                'code': 0,
                'host_len': host_len_msg,
                'user_len': user_len_msg,
                'group_len': group_len_msg,
                'container_len': 0
            })
        except IOError:
            return jsonify({'code': 1})

    @property
    def server_list(self):
        try:
            host_id = request.values.get("id")
            query_msg = t_host.query.filter_by(id=host_id).first()
            list_msg = self.lt.dict_reset_pop(query_msg)
            return jsonify(list_msg)
        except IOError:
            return jsonify({"host_list_msg": 'select list msg error'})

    @property
    def server_list_page(self):
        table_page = request.values.get('page')
        table_limit = request.values.get('limit')
        table_offset = (int(table_page) - 1) * 10
        group_name = request.values.get('group_name')
        try:
            if group_name == '所有资产':
                return self.server_list_all
            else:
                query_msg = t_host.query.filter_by(group=group_name).offset(table_offset).limit(table_limit).all()
                list_msg = self.lt.dict_ls_reset_dict(query_msg)
                len_msg = t_host.query.filter_by(group=group_name).count()
                return jsonify({"host_status": 0,
                                "host_list_msg": list_msg,
                                "msg": "",
                                "host_len_msg": len_msg})
        except IOError:
            return jsonify({"host_list_msg": 'select list msg error',
                            "host_len_msg": 0})

    @property
    def server_list_all(self):
        try:
            table_page = request.values.get('page')
            table_limit = request.values.get('limit')
            table_offset = (int(table_page) - 1) * 10
            name = request.values.get('name')
            que_auth_group = t_auth_host.query.filter(t_auth_host.user.like("%{}%".format(name))).all()
            auth_group = self.lt.auth_ls_list_que(que_auth_group)
            query_msg = t_host.query.filter(t_host.group.in_(auth_group)).offset(table_offset).limit(table_limit).all()
            list_msg = self.lt.dict_ls_reset_dict(query_msg)
            len_msg = t_host.query.filter(t_host.group.in_(auth_group)).count()
            return jsonify({"host_status": 0,
                            "host_list_msg": list_msg,
                            "msg": "",
                            "host_len_msg": len_msg})
        except IOError:
            return jsonify({"host_list_msg": 'select list msg error',
                            "host_len_msg": 0})


class GroupList:
    def __init__(self):
        self.group = request.values.get('group')
        self.lt = ListTool()

    @property
    def server_list(self):
        try:
            group_list = t_host.query.filter_by(group=self.group).all()
            len_msg = t_host.query.filter_by(group=self.group).count()
            group_select = self.lt.dict_ls_reset_list(group_list)
            return jsonify({"group_list_msg": group_select,
                            "group_len_msg": len_msg})

        except IOError:
            return jsonify({"group_list_msg": 'select group list msg error',
                            "group_len_msg": 0})


class ServerDel:
    def __init__(self):
        # self.host_ip = request.values.get('host_ip')
        self.id = request.values.get('id')
        # 新增记录日志相关
        self.cz_name = request.values.get('cz_name')
        self.new_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.cz_ins = CzLogSqlalh()

    @property
    def host_del(self):
        # user_chk = Host.query.filter_by(host_ip=self.host_ip).first()
        user_chk = t_host.query.filter_by(id=self.id).first()
        if user_chk:
            db.session.delete(user_chk)
            db.session.commit()
            self.cz_ins.ins_sql(self.cz_name, '资产操作', '删除资产', self.id, '成功', None, self.new_date)
            return jsonify({'server_del_status': 'true'})
        else:
            self.cz_ins.ins_sql(self.cz_name, '资产操作', '删除资产', self.id, '失败', '系统内没有该资产', self.new_date)
            return jsonify({'server_del_status': 'fail'})


class ServerAdd:
    def __init__(self):
        self.alias = request.values.get('alias')
        self.host_ip = request.values.get('host_ip')
        self.host_port = request.values.get('host_port')
        self.host_user = request.values.get('host_user')
        self.host_password = request.values.get('host_password')
        self.group = request.values.get('group', type=str, default='default')
        self.host_sqlalh = HostSqlalh()
        self.basesec = BaseSec()
        # 新增记录日志相关
        self.cz_name = request.values.get('cz_name')
        self.new_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.cz_ins = CzLogSqlalh()

    @property
    def host_add(self):
        try:
            user_chk = t_host.query.filter_by(host_ip=self.host_ip).first()
            if user_chk is None:
                password_en = self.basesec.base_en(self.host_password)
                conn = RemoteConnection(self.host_ip, int(self.host_port), self.host_user, self.host_password)
                conn.ssh_cmd('hostname')
                self.host_sqlalh.ins_sql(self.alias, self.host_ip, self.host_port, self.host_user, password_en,
                                         self.group)
                self.cz_ins.ins_sql(self.cz_name, '资产操作', '新增资产', self.alias, '成功', None, self.new_date)
                return jsonify({'server_add_status': 'true'})
            else:
                self.cz_ins.ins_sql(self.cz_name, '资产操作', '新增资产', self.alias, '失败', '该资产已存在', self.new_date)
                return jsonify({'server_add_status': 'sel_fail'})
        except IOError:
            self.cz_ins.ins_sql(self.cz_name, '资产操作', '新增资产', self.alias, '失败', '连接主机失败', self.new_date)
            return jsonify({'server_add_status': 'con_fail'})
        except Exception:
            self.cz_ins.ins_sql(self.cz_name, '资产操作', '新增资产', self.alias, '失败', '未知错误', self.new_date)
            return jsonify({'server_add_status': 'fail'})


class ServerUpdate(ServerAdd):
    def __init__(self):
        super(ServerUpdate, self).__init__()
        self.id = request.values.get('id')

    @property
    def update(self):
        try:
            conn = RemoteConnection(self.host_ip, int(self.host_port), self.host_user, self.host_password)
            conn.ssh_cmd('hostname')
            try:
                password_en = self.basesec.base_en(self.host_password)
                t_host.query.filter_by(id=self.id).update({'alias': self.alias, 'host_ip': self.host_ip,
                                                           'host_port': self.host_port,
                                                           'host_user': self.host_user,
                                                           'host_password': password_en, 'group': self.group})
                db.session.commit()
                self.cz_ins.ins_sql(self.cz_name, '资产操作', '变更资产', self.alias, '成功', None, self.new_date)
                return jsonify({'server_ping_status': 'true',
                                'server_into_update': 'true'})
            except Exception:
                self.cz_ins.ins_sql(self.cz_name, '资产操作', '变更资产', self.alias, '失败', '连接数据库错误', self.new_date)
                return jsonify({'server_into_update': 'fail'})
        except Exception:
            self.cz_ins.ins_sql(self.cz_name, '资产操作', '变更资产', self.alias, '失败', '未知错误', self.new_date)
            return jsonify({'server_ping_status': 'fail'})


class ServerCmd(ServerAdd):
    def __init__(self):
        super(ServerCmd, self).__init__()
        self.command = request.values.get('command')

    @property
    def sh_cmd(self):
        try:
            conn = RemoteConnection(self.host_ip, int(self.host_port), self.host_user, self.host_password)
            msg = conn.ssh_cmd(self.command)
            return jsonify({'server_ping_status': 'true',
                            'command_msg': msg})
        except IOError:
            return jsonify({'server_ping_status': 'fail'})


class ServerCmd2:
    def __init__(self):
        # self.host_ip = request.values.get('host_ip')
        self.host_id = request.values.get('host_id')
        self.command = request.values.get('command')
        self.basesec = BaseSec()

    @property
    def sh_cmd(self):
        try:
            host = t_host.query.filter_by(id=self.host_id).first()
            host_dict = host.__dict__
            password_de = self.basesec.base_de(host_dict['host_password'])
            conn = RemoteConnection(host_dict['host_ip'], host_dict['host_port'], host_dict['host_user'], password_de)
            msg = conn.ssh_cmd(self.command)
            return jsonify({'server_ping_status': 'true',
                            'command_msg': msg,
                            'hostname_list': self.host_id})
        except IOError:
            return jsonify({'server_ping_status': 'fail'})


class ServerListCmd(ServerCmd2):
    def __init__(self):
        super(ServerListCmd, self).__init__()
        # self.host_ip = request.values.getlist('host_ip')
        self.host_id = request.values.getlist('host_id')

        self.new_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.com_name = request.values.get('com_name')
        self.com_ins = CommandLogSqlalh
        self.com_host = ','.join(self.host_id)

    @property
    def sh_list_cmd(self):
        msg_list = []
        alias_list = []
        error_list = []
        for hid in self.host_id:
            host = t_host.query.filter_by(id=hid).first()
            host_dict = host.__dict__
            password_de = self.basesec.base_de(host_dict['host_password'])
            try:
                conn = RemoteConnection(host_dict['host_ip'], host_dict['host_port'], host_dict['host_user'],
                                        password_de)
                msg = conn.ssh_cmd(self.command)
                msg_list.append(msg)
                alias_list.append(host_dict['alias'])
            except IOError:
                error_list.append(host_dict['alias'])
        if len(error_list) == 0:
            self.com_ins.ins_sql(self.com_name, '批量命令', self.command, self.com_host, '成功', None, self.new_date)
            return jsonify({'server_ping_status': 'true',
                            'command_msg': msg_list,
                            'hostname_list': alias_list})
        else:
            self.com_ins.ins_sql(self.com_name, '批量命令', self.command, self.com_host, '失败', '连接主机失败', self.new_date)
            return jsonify({'server_ping_status': 'fail',
                            'error_list': error_list,
                            'msg': 'host connect to timeout!'})


class GroupCmd:
    def __init__(self):
        self.group = request.values.get('group')
        self.command = request.values.get('command')
        self.basesec = BaseSec()

    @property
    def sh_cmd(self):
        try:
            msg_list = []
            group_list = t_host.query.filter_by(group=self.group).all()
            group_in_host_list = []
            for groups in group_list:
                group_dict = groups.__dict__
                password_de = self.basesec.base_de(group_dict['host_password'])
                conn = RemoteConnection(group_dict['host_ip'], group_dict['host_port'], group_dict['host_user'],
                                        password_de)
                msg = conn.ssh_cmd(self.command)
                msg_list.append(msg)
                group_in_host_list.append(group_dict['host_ip'])
            return jsonify({'group_ping_status': 'true',
                            'command_msg': msg_list,
                            'group_list': self.group,
                            'hostname_list': group_in_host_list})
        except IOError:
            return jsonify({'group_ping_status': 'fail'})


class GroupListCmd(GroupCmd):
    def __init__(self):
        super(GroupListCmd, self).__init__()
        self.group_ls = request.values.getlist('group_ls')

    @property
    def sh_list_cmd(self):
        # 实际能否批量执行组内主机未测试
        try:
            gop_list_msg = []
            for group in self.group_ls:
                msg_list = []
                group_list = t_host.query.filter_by(group=group).all()
                for groups in group_list:
                    group_dict = groups.__dict__
                    password_de = self.basesec.base_de(group_dict['host_password'])
                    conn = RemoteConnection(group_dict['host_ip'], group_dict['host_port'], group_dict['host_user'],
                                            password_de)
                    msg = conn.ssh_cmd(self.command)
                    msg_list.append(msg)
                msg_dict = {group: msg_list}
                gop_list_msg.append(msg_dict)
            return jsonify({'server_ping_status': 'true',
                            'command_msg': gop_list_msg})
        except IOError:
            return jsonify({'server_ping_status': 'fail'})


# 脚本上传接口
class ServerScript:
    def __init__(self):
        self.file = request.files.get('file')
        # self.rem = RemoteConnection('10.0.1.199', 22, 'root', 'jlb123')
        self.id_list = request.values.getlist('id_list')
        self.basesec = BaseSec()
        self.local_cmd = LocalShell()
        self.filename = secure_filename(self.file.filename)
        self.on_file = '/data/putfile/' + self.filename
        self.to_file = '/tmp/' + self.filename

        self.new_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.com_name = request.values.get('com_name')
        self.com_ins = CommandLogSqlalh
        self.com_host = ','.join(self.id_list)

    def sh_script(self):
        self.file.save(self.on_file)
        msg_list = []
        alias_list = []
        error_list = []
        for hid in self.id_list:
            host = t_host.query.filter_by(id=hid).first()
            host_dict = host.__dict__
            password_de = self.basesec.base_de(host_dict['host_password'])
            try:
                conn = RemoteConnection(host_dict['host_ip'], host_dict['host_port'], host_dict['host_user'],
                                        password_de)
                conn.put_file(self.on_file, self.to_file)
                msg = conn.ssh_cmd("chmod +x %s && %s" % (self.to_file, self.to_file))
                msg_list.append(msg)
                alias_list.append(host_dict['alias'])
                conn.ssh_cmd("rm -f %s" % self.to_file)
            except IOError:
                error_list.append(host_dict['alias'])
        if len(error_list) == 0:
            self.com_ins.ins_sql(self.com_name, '批量脚本', self.filename, self.com_host, '成功', None, self.new_date)
            self.local_cmd.cmd_shell("rm -f %s" % self.on_file)
            return jsonify({'server_ping_status': 'true',
                            'command_msg': msg_list,
                            'hostname_list': alias_list})
        else:
            self.com_ins.ins_sql(self.com_name, '批量脚本', self.filename, self.com_host, '失败', '连接主机失败', self.new_date)
            return jsonify({'server_ping_status': 'fail',
                            'error_list': error_list,
                            'msg': 'host connect to timeout!'})


if __name__ == "__main__":
    slist = ServerList()
    slist.server_list()
