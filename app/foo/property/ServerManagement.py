from flask import request, jsonify
from app.tools.shellcmd import RemoteConnection
from app.sqldb.SqlAlchemyDB import Host, db, t_group, t_sys_user, User2
from app.sqldb.SqlAlchemyInsert import HostSqlalh
from app.tools.SqlListTool import ListTool
from app.tools.basesec import BaseSec


class ServerList:
    def __init__(self):
        self.ls_tool = ListTool()

    @property
    def server_count_all(self):
        try:
            host_len_msg = Host.query.count()
            user_len_msg = User2.query.count()
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
            query_msg = Host.query.filter_by(id=host_id).first()
            list_msg = self.ls_tool.dict_reset_pop(query_msg)
            return jsonify(list_msg)
        except IOError:
            return jsonify({"host_list_msg": 'select list msg error'})

    @property
    def server_list_page(self):
        group_name = request.values.get('group_name')
        try:
            if group_name == '所有资产':
                return self.server_list_all
            else:
                query_msg = Host.query.filter_by(group=group_name).all()
                list_msg = self.ls_tool.dict_ls_reset_dict(query_msg)
                len_msg = Host.query.filter_by(group=group_name).count()
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
            query_msg = Host.query.all()
            list_msg = self.ls_tool.dict_ls_reset_dict(query_msg)
            len_msg = Host.query.count()
            return jsonify({"host_status": 0,
                            "host_list_msg": list_msg,
                            "msg": "",
                            "host_len_msg": len_msg})
            # return jsonify({"code": 0,
            #                 "count": len_msg,
            #                 "msg": "",
            #                 "data": list_msg})
        except IOError:
            return jsonify({"host_list_msg": 'select list msg error',
                            "host_len_msg": 0})


class GroupList:
    def __init__(self):
        self.group = request.values.get('group')
        self.ls_tool = ListTool()

    @property
    def server_list(self):
        try:
            group_list = Host.query.filter_by(group=self.group).all()
            len_msg = Host.query.filter_by(group=self.group).count()
            group_select = self.ls_tool.dict_ls_reset_list(group_list)
            return jsonify({"group_list_msg": group_select,
                            "group_len_msg": len_msg})

        except IOError:
            return jsonify({"group_list_msg": 'select group list msg error',
                            "group_len_msg": 0})


class ServerDel:
    def __init__(self):
        # self.host_ip = request.values.get('host_ip')
        self.id = request.values.get('id')

    @property
    def host_del(self):
        # user_chk = Host.query.filter_by(host_ip=self.host_ip).first()
        user_chk = Host.query.filter_by(id=self.id).first()
        if not user_chk is None:
            db.session.delete(user_chk)
            db.session.commit()
            return jsonify({'server_del_status': 'true'})
        else:
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

    @property
    def host_add(self):
        try:
            user_chk = Host.query.filter_by(host_ip=self.host_ip).first()
            if user_chk is None:
                password_en = self.basesec.base_en(self.host_password)
                conn = RemoteConnection(self.host_ip, int(self.host_port), self.host_user, self.host_password)
                conn.ssh_cmd('hostname')
                self.host_sqlalh.ins_sql(self.alias, self.host_ip, self.host_port, self.host_user, password_en,
                                         self.group)
                return jsonify({'server_add_status': 'true'})
            else:
                return jsonify({'server_add_status': 'sel_fail'})
        except IOError:
            return jsonify({'server_add_status': 'con_fail'})
        except Exception:
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
                Host.query.filter_by(id=self.id).update({'alias': self.alias, 'host_ip': self.host_ip,
                                                         'host_port': self.host_port,
                                                         'host_user': self.host_user,
                                                         'host_password': password_en, 'group': self.group})
                db.session.commit()
                return jsonify({'server_ping_status': 'true',
                                'server_into_update': 'true'})
            except Exception:
                return jsonify({'server_into_update': 'fail'})
        except Exception:
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
            host = Host.query.filter_by(id=self.host_id).first()
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

    @property
    def sh_list_cmd(self):
        try:
            msg_list = []
            alias_list = []
            for hid in self.host_id:
                host = Host.query.filter_by(id=hid).first()
                host_dict = host.__dict__
                password_de = self.basesec.base_de(host_dict['host_password'])
                conn = RemoteConnection(host_dict['host_ip'], host_dict['host_port'], host_dict['host_user'],
                                        password_de)
                msg = conn.ssh_cmd(self.command)
                msg_list.append(msg)
                alias_list.append(host_dict['alias'])
            return jsonify({'server_ping_status': 'true',
                            'command_msg': msg_list,
                            'hostname_list': alias_list})
        except IOError:
            return jsonify({'server_ping_status': 'fail'})


class GroupCmd:
    def __init__(self):
        self.group = request.values.get('group')
        self.command = request.values.get('command')
        self.basesec = BaseSec()

    @property
    def sh_cmd(self):
        try:
            msg_list = []
            group_list = Host.query.filter_by(group=self.group).all()
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
                group_list = Host.query.filter_by(group=group).all()
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


# 修改主机值初版，待优化
# class UpdateHost:
#     def __init__(self):
#         self.host_ip = request.values.get("host_ip")
#         self.setval = request.values.get('setval')
#         self.basesec = BaseSec()
#
#     def set_host(self):
#         for i in self.setval.keys():
#             try:
#                 if i == 'host_password':
#                     password_en = self.basesec.base_en(self.setval[i])
#                     Host.query.filter_by(host_ip=self.host_ip).update({i: password_en})
#                 else:
#                     Host.query.filter_by(host_ip=self.host_ip).update({i: self.setval[i]})
#                 return jsonify({'server_ping_status': 'true'})
#             except IOError:
#                 return jsonify({'server_ping_status': 'fail'})


if __name__ == "__main__":
    slist = ServerList()
    slist.server_list()
