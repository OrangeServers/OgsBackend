from flask import request, jsonify
from app.tools.basesec import BaseSec
from app.tools.SqlListTool import ListTool
from app.sqldb.SqlAlchemyDB import t_group, t_auth_host, db
from app.sqldb.SqlAlchemyInsert import GroupSqlalh


class ServerGroupList:
    def __init__(self):
        self.lt = ListTool()

    @property
    def group_list(self):
        try:
            group_id = request.values.get("id")
            query_msg = t_group.query.filter_by(id=group_id).first()
            list_msg = self.lt.dict_reset_pop_auto(query_msg)
            return jsonify(list_msg)
        except IOError:
            return jsonify({"server_group_list_msg": 'select list msg error'})

    @property
    def group_name_list(self):
        name = request.values.get('name')
        try:
            que_auth_group = t_auth_host.query.filter(t_auth_host.user.like("%{}%".format(name))).all()
            auth_group = self.lt.auth_ls_list_que(que_auth_group)
            group_list = list(auth_group)
            return jsonify({'group_name_list_msg': group_list})
        except IOError:
            return jsonify({'get_name_list': 'fail'})

    @property
    def group_list_all(self):
        try:
            table_page = request.values.get('page')
            table_limit = request.values.get('limit')
            table_offset = (int(table_page) - 1) * 10
            query_msg = t_group.query.offset(table_offset).limit(table_limit).all()
            list_msg = self.lt.dict_ls_reset_dict_auto(query_msg)
            len_msg = t_group.query.count()
            return jsonify({"host_status": 0,
                            "group_list_msg": list_msg,
                            "msg": "",
                            "group_len_msg": len_msg})
        except IOError:
            return jsonify({"host_list_msg": 'select list msg error',
                            "host_len_msg": 0})


class ServerGroupDel:
    def __init__(self):
        self.id = request.values.get('id')

    @property
    def host_del(self):
        user_chk = t_group.query.filter_by(id=self.id).first()
        if not user_chk is None:
            db.session.delete(user_chk)
            db.session.commit()
            return jsonify({'server_group_del_status': 'true'})
        else:
            return jsonify({'server_group_del_status': 'fail'})


class ServerGroupAdd:
    def __init__(self):
        self.name = request.values.get('name')
        self.remarks = request.values.get('remarks', type=str, default=None)
        self.host_sqlalh = GroupSqlalh()
        self.basesec = BaseSec()

    @property
    def host_add(self):
        try:
            user_chk = t_group.query.filter_by(name=self.name).first()
            if user_chk is None:
                self.host_sqlalh.ins_sql(self.name, self.remarks)
                return jsonify({'server_group_add_status': 'true'})
            else:
                return jsonify({'server_group_add_status': 'sel_fail'})
        except IOError:
            return jsonify({'server_group_add_status': 'con_fail'})
        except Exception:
            return jsonify({'server_group_add_status': 'fail'})


class ServerGroupUpdate(ServerGroupAdd):
    def __init__(self):
        super(ServerGroupUpdate, self).__init__()
        self.id = request.values.get('id')

    @property
    def update(self):
        try:
            t_group.query.filter_by(id=self.id).update({'name': self.name, 'nums': self.nums, 'remarks': self.remarks})
            db.session.commit()
            return jsonify({'server_group_ping_status': 'true',
                            'server_group_into_update': 'true'})
        except Exception:
            return jsonify({'server_group_into_update': 'fail'})