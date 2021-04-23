from flask import request, jsonify
from app.tools.basesec import BaseSec
from app.tools.SqlListTool import ListTool
from app.sqldb.SqlAlchemyDB import t_acc_user, db
from app.sqldb.SqlAlchemyInsert import AccUserSqlalh


class AccUserList:
    def __init__(self):
        self.lt = ListTool()

    @property
    def sys_user_list(self):
        try:
            acc_user_id = request.values.get("id")
            query_msg = t_acc_user.query.filter_by(id=acc_user_id).first()
            list_msg = self.lt.dict_reset_pop_auto(query_msg, 'password')
            return jsonify(list_msg)
        except IOError:
            return jsonify({"acc_user_list_msg": 'select list msg error'})

    @property
    def sys_user_list_all(self):
        try:
            query_msg = t_acc_user.query.all()
            list_msg = self.lt.dict_ls_reset_dict_auto(query_msg, 'password')
            len_msg = t_acc_user.query.count()
            return jsonify({"host_status": 0,
                            "acc_user_list_msg": list_msg,
                            "msg": "",
                            "acc_user_len_msg": len_msg})
        except IOError:
            return jsonify({"acc_user_list_msg": 'select list msg error',
                            "acc_user_len_msg": 0})


class AccUserDel:
    def __init__(self):
        # self.host_ip = request.values.get('host_ip')
        self.id = request.values.get('id')

    @property
    def host_del(self):
        # user_chk = Host.query.filter_by(host_ip=self.host_ip).first()
        user_chk = t_acc_user.query.filter_by(id=self.id).first()
        if not user_chk is None:
            db.session.delete(user_chk)
            db.session.commit()
            return jsonify({'acc_user_del_status': 'true'})
        else:
            return jsonify({'acc_user_del_status': 'fail'})


class AccUserAdd:
    def __init__(self):
        self.alias = request.values.get('alias')
        self.name = request.values.get('name')
        self.password = request.values.get('password')
        self.usrole = request.values.get('usrole')
        self.mail = request.values.get('mail')
        self.remarks = request.values.get('remarks', type=str, default=None)
        self.host_sqlalh = AccUserSqlalh()
        self.basesec = BaseSec()

    @property
    def host_add(self):
        try:
            user_chk = t_acc_user.query.filter_by(name=self.name).first()
            if user_chk is None:
                password_en = self.basesec.base_en(self.password)
                self.host_sqlalh.ins_sql(self.alias, self.name, password_en, self.usrole, self.mail,
                                         self.remarks)
                return jsonify({'acc_user_add_status': 'true'})
            else:
                return jsonify({'acc_user_add_status': 'sel_fail'})
        except IOError:
            return jsonify({'acc_user_add_status': 'con_fail'})
        except Exception:
            return jsonify({'acc_user_add_status': 'fail'})


class AccUserUpdate(AccUserAdd):
    def __init__(self):
        super(AccUserUpdate, self).__init__()
        self.id = request.values.get('id')

    @property
    def update(self):
        try:
            password_en = self.basesec.base_en(self.password)
            t_acc_user.query.filter_by(id=self.id).update({'alias': self.alias, 'name': self.name,
                                                           'password': password_en,
                                                           'usrole': self.usrole,
                                                           'mail': self.mail, 'remarks': self.remarks})
            db.session.commit()
            return jsonify({'acc_user_ping_status': 'true',
                            'acc_user_into_update': 'true'})
        except Exception:
            return jsonify({'acc_user_into_update': 'fail'})