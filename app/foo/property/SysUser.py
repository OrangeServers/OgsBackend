from flask import request, jsonify
from app.sqldb.SqlAlchemyDB import t_sys_user, db
from app.sqldb.SqlAlchemyInsert import SysUserSqlalh
from app.tools.SqlListTool import ListTool
from app.tools.basesec import BaseSec


class SysUserList:
    def __init__(self):
        self.ls_tool = ListTool()

    @property
    def sys_user_list(self):
        try:
            sys_user_id = request.values.get("id")
            query_msg = t_sys_user.query.filter_by(id=sys_user_id).first()
            list_msg = self.ls_tool.dict_reset_pop(query_msg)
            return jsonify(list_msg)
        except IOError:
            return jsonify({"sys_user_list_msg": 'select list msg error'})

    @property
    def sys_user_list_all(self):
        try:
            query_msg = t_sys_user.query.all()
            list_msg = self.ls_tool.dict_ls_reset_dict_auto(query_msg, 'host_password')
            len_msg = t_sys_user.query.count()
            return jsonify({"host_status": 0,
                            "sys_user_list_msg": list_msg,
                            "msg": "",
                            "sys_user_len_msg": len_msg})
        except IOError:
            return jsonify({"sys_user_list_msg": 'select list msg error',
                            "sys_user_len_msg": 0})


class SysUserDel:
    def __init__(self):
        # self.host_ip = request.values.get('host_ip')
        self.id = request.values.get('id')

    @property
    def host_del(self):
        # user_chk = Host.query.filter_by(host_ip=self.host_ip).first()
        user_chk = t_sys_user.query.filter_by(id=self.id).first()
        if not user_chk is None:
            db.session.delete(user_chk)
            db.session.commit()
            return jsonify({'sys_user_del_status': 'true'})
        else:
            return jsonify({'sys_user_del_status': 'fail'})


class SysUserAdd:
    def __init__(self):
        self.alias = request.values.get('alias')
        self.host_user = request.values.get('host_user')
        self.host_password = request.values.get('host_password')
        self.agreement = request.values.get('agreement')
        self.remarks = request.values.get('remarks', type=str, default=None)
        self.host_sqlalh = SysUserSqlalh()
        self.basesec = BaseSec()

    @property
    def host_add(self):
        try:
            user_chk = t_sys_user.query.filter_by(alias=self.alias).first()
            if user_chk is None:
                password_en = self.basesec.base_en(self.host_password)
                self.host_sqlalh.ins_sql(self.alias, self.host_user, password_en, self.agreement, self.remarks)
                return jsonify({'sys_user_add_status': 'true'})
            else:
                return jsonify({'sys_user_add_status': 'sel_fail'})
        except IOError:
            return jsonify({'sys_user_add_status': 'con_fail'})
        except Exception:
            return jsonify({'sys_user_add_status': 'fail'})


class SysUserUpdate(SysUserAdd):
    def __init__(self):
        super(SysUserUpdate, self).__init__()
        self.id = request.values.get('id')

    @property
    def update(self):
        try:
            password_en = self.basesec.base_en(self.host_password)
            t_sys_user.query.filter_by(id=self.id).update({'alias': self.alias, 'host_user': self.host_user,
                                                           'host_password': password_en,
                                                           'agreement': self.agreement,
                                                           'nums': self.nums, 'remarks': self.remarks})
            db.session.commit()
            return jsonify({'sys_user_ping_status': 'true',
                            'sys_user_into_update': 'true'})
        except Exception:
            return jsonify({'sys_user_into_update': 'fail'})
