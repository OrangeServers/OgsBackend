from flask import request, jsonify
from app.tools.SqlListTool import ListTool
from app.sqldb.SqlAlchemyDB import t_auth_host, t_group, t_acc_user, t_sys_user, t_acc_group, db
from app.sqldb.SqlAlchemyInsert import AuthHostSqlalh


class AuthHostList:
    def __init__(self):
        self.lt = ListTool()

    @property
    def create_auth_list(self):
        req_type = request.values.get("req_type")
        auth_list = []
        if req_type == 'user':
            query_user_name = t_acc_user.query.with_entities(t_acc_user.name).all()
            user_name = self.lt.list_gather(query_user_name)
            for i in user_name:
                auth_list.append({'name': i, 'value': i})
            return jsonify({'msg': auth_list})

        elif req_type == 'user_group':
            query_group_name = t_acc_group.query.with_entities(t_acc_group.name).all()
            group_name = self.lt.list_gather(query_group_name)
            for i in group_name:
                auth_list.append({'name': i, 'value': i})
            return jsonify({'msg': auth_list})

        elif req_type == 'host_group':
            query_group_name = t_group.query.with_entities(t_group.name).all()
            group_name = self.lt.list_gather(query_group_name)
            for i in group_name:
                auth_list.append({'name': i, 'value': i})
            return jsonify({'msg': auth_list})

        elif req_type == 'sys_user':
            query_user_name = t_sys_user.query.with_entities(t_sys_user.alias).all()
            user_name = self.lt.list_gather(query_user_name)
            for i in user_name:
                auth_list.append({'name': i, 'value': i})
            return jsonify({'msg': auth_list})

    @property
    def auth_group_role(self):
        auth_name = request.values.get('name')
        req_type = request.values.get("req_type")
        auth_list = []
        if req_type == 'all':
            try:
                query_auth_msg = t_auth_host.query.filter_by(name=auth_name).first()
                return jsonify({'name': query_auth_msg.name, 'remarks': query_auth_msg.remarks})
            except IOError:
                return jsonify({'msg': 'fail'})

        elif req_type == 'user':
            try:
                query_user_name = t_acc_user.query.with_entities(t_acc_user.name).all()
                user_name = self.lt.list_gather(query_user_name)
                query_auth_msg = t_auth_host.query.filter_by(name=auth_name).first()
                auth_msg = query_auth_msg.user
                if auth_msg is None:
                    auth_msg = ''
                auth_msg_list = auth_msg.split(',')
                for i in user_name:
                    if i in auth_msg_list:
                        auth_list.append({'name': i, 'value': i, 'selected': 'selected'})
                    else:
                        auth_list.append({'name': i, 'value': i})
                return jsonify({'msg': auth_list})
            except IOError:
                return jsonify({'msg': 'fail'})

        elif req_type == 'user_group':
            try:
                query_group_name = t_acc_group.query.with_entities(t_acc_group.name).all()
                group_name = self.lt.list_gather(query_group_name)
                query_auth_msg = t_auth_host.query.filter_by(name=auth_name).first()
                auth_msg = query_auth_msg.user_group
                if auth_msg is None:
                    auth_msg = ''
                auth_msg_list = auth_msg.split(',')
                for i in group_name:
                    if i in auth_msg_list:
                        auth_list.append({'name': i, 'value': i, 'selected': 'selected'})
                    else:
                        auth_list.append({'name': i, 'value': i})
                return jsonify({'msg': auth_list})
            except IOError:
                return jsonify({'msg': 'fail'})

        elif req_type == 'host_group':
            try:
                query_group_name = t_group.query.with_entities(t_group.name).all()
                group_name = self.lt.list_gather(query_group_name)
                query_auth_msg = t_auth_host.query.filter_by(name=auth_name).first()
                auth_msg = query_auth_msg.host_group
                if auth_msg is None:
                    auth_msg = ''
                auth_msg_list = auth_msg.split(',')
                for i in group_name:
                    if i in auth_msg_list:
                        auth_list.append({'name': i, 'value': i, 'selected': 'selected'})
                    else:
                        auth_list.append({'name': i, 'value': i})
                return jsonify({'msg': auth_list})
            except IOError:
                return jsonify({'msg': 'fail'})

        elif req_type == 'sys_user':
            try:
                query_user_name = t_sys_user.query.with_entities(t_sys_user.alias).all()
                user_name = self.lt.list_gather(query_user_name)
                query_auth_msg = t_auth_host.query.filter_by(name=auth_name).first()
                auth_msg = query_auth_msg.sys_user
                if auth_msg is None:
                    auth_msg = ''
                auth_msg_list = auth_msg.split(',')
                for i in user_name:
                    if i in auth_msg_list:
                        auth_list.append({'name': i, 'value': i, 'selected': 'selected'})
                    else:
                        auth_list.append({'name': i, 'value': i})
                return jsonify({'msg': auth_list})
            except IOError:
                return jsonify({'msg': 'fail'})

    @property
    def auth_host_list(self):
        try:
            acc_user_id = request.values.get("id")
            query_msg = t_auth_host.query.filter_by(id=acc_user_id).first()
            list_msg = self.lt.dict_reset_pop_auto(query_msg)
            return jsonify(list_msg)
        except IOError:
            return jsonify({"auth_host_list_msg": 'select list msg error'})

    @property
    def auth_host_list_all(self):
        try:
            table_page = request.values.get('page')
            table_limit = request.values.get('limit')
            table_offset = (int(table_page) - 1) * 10
            query_msg = t_auth_host.query.offset(table_offset).limit(table_limit).all()
            list_msg = self.lt.dict_ls_reset_dict_auto(query_msg)
            len_msg = t_auth_host.query.count()
            return jsonify({"code": 0,
                            "auth_host_list_msg": list_msg,
                            "msg": "",
                            "auth_host_len_msg": len_msg})
        except IOError:
            return jsonify({"auth_host_list_msg": 'select list msg error',
                            "auth_host_len_msg": 0})


class AuthHostDel:
    def __init__(self):
        # self.host_ip = request.values.get('host_ip')
        self.name = request.values.get('name')

    @property
    def auth_host_del(self):
        # user_chk = Host.query.filter_by(host_ip=self.host_ip).first()
        auth_chk = t_auth_host.query.filter_by(name=self.name).first()
        if auth_chk:
            if self.name != '所有权限':
                db.session.delete(auth_chk)
                db.session.commit()
                return jsonify({'code': 0})
            elif self.name == '所有权限':
                return jsonify({'code': 131})
        else:
            return jsonify({'code': 2})


class AuthHostAdd:
    def __init__(self):
        self.name = request.values.get('name')
        self.user = request.values.get('user')
        self.user_group = request.values.get('user_group')
        self.host_group = request.values.get('host_group')
        self.sys_user = request.values.get('sys_user')
        self.remarks = request.values.get('remarks', type=str, default=None)
        self.auth_sqlalh = AuthHostSqlalh()

    @property
    def auth_host_add(self):
        try:
            auth_chk = t_auth_host.query.filter_by(name=self.name).first()
            if auth_chk is None:
                self.auth_sqlalh.ins_sql(self.name, self.user, self.user_group, self.host_group, self.sys_user,
                                         self.remarks)
                return jsonify({'code': 0})
            else:
                return jsonify({'code': 132})
        except IOError:
            return jsonify({'code': 201})
        except Exception:
            return jsonify({'code': 2})


class AuthHostUpdate(AuthHostAdd):
    def __init__(self):
        super(AuthHostUpdate, self).__init__()
        self.id = request.values.get('name')

    @property
    def auth_host_update(self):
        try:
            t_auth_host.query.filter_by(name=self.name).update({'name': self.name, 'user': self.user,
                                                                'user_group': self.user_group,
                                                                'host_group': self.host_group,
                                                                'sys_user': self.sys_user,
                                                                'remarks': self.remarks})
            db.session.commit()
            return jsonify({'code': 0})
        except Exception:
            return jsonify({'code': 2})
