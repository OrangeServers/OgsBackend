from flask import request, jsonify
from app.tools.SqlListTool import ListTool
from app.sqldb.SqlAlchemyDB import t_auth_host, db
from app.sqldb.SqlAlchemyInsert import AuthHostSqlalh


class AuthHostList:
    def __init__(self):
        self.lt = ListTool()

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
            query_msg = t_auth_host.query.all()
            list_msg = self.lt.dict_ls_reset_dict_auto(query_msg)
            len_msg = t_auth_host.query.count()
            return jsonify({"host_status": 0,
                            "auth_host_list_msg": list_msg,
                            "msg": "",
                            "auth_host_len_msg": len_msg})
        except IOError:
            return jsonify({"auth_host_list_msg": 'select list msg error',
                            "auth_host_len_msg": 0})


class AuthHostDel:
    def __init__(self):
        # self.host_ip = request.values.get('host_ip')
        self.id = request.values.get('id')

    @property
    def auth_host_del(self):
        # user_chk = Host.query.filter_by(host_ip=self.host_ip).first()
        auth_chk = t_auth_host.query.filter_by(id=self.id).first()
        if not auth_chk is None:
            db.session.delete(auth_chk)
            db.session.commit()
            return jsonify({'auth_host_del_status': 'true'})
        else:
            return jsonify({'auth_host_del_status': 'fail'})


class AuthHostAdd:
    def __init__(self):
        self.name = request.values.get('name')
        self.user = request.values.get('user')
        self.user_group = request.values.get('user_group')
        self.host_group = request.values.get('host_group')
        self.remarks = request.values.get('remarks', type=str, default=None)
        self.auth_sqlalh = AuthHostSqlalh()

    @property
    def auth_host_add(self):
        try:
            auth_chk = t_auth_host.query.filter_by(name=self.name).first()
            if auth_chk is None:
                self.auth_sqlalh.ins_sql(self.name, self.user, self.user_group, self.host_group, self.remarks)
                return jsonify({'auth_host_add_status': 'true'})
            else:
                return jsonify({'auth_host_add_status': 'sel_fail'})
        except IOError:
            return jsonify({'auth_host_add_status': 'con_fail'})
        except Exception:
            return jsonify({'auth_host_add_status': 'fail'})


class AuthHostUpdate(AuthHostAdd):
    def __init__(self):
        super(AuthHostUpdate, self).__init__()
        self.id = request.values.get('id')

    @property
    def auth_host_update(self):
        try:
            t_auth_host.query.filter_by(id=self.id).update({'name': self.name, 'user': self.user,
                                                            'user_group': self.user_group,
                                                            'host_group': self.host_group,
                                                            'remarks': self.remarks})
            db.session.commit()
            return jsonify({'auth_host_ping_status': 'true',
                            'auth_host_into_update': 'true'})
        except Exception:
            return jsonify({'auth_host_into_update': 'fail'})