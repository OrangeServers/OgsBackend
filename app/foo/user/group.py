from flask import request, jsonify
from app.tools.basesec import BaseSec
from app.tools.SqlListTool import ListTool
from app.sqldb.SqlAlchemySettings import db
from app.sqldb.SqlAlchemyDB import t_group


class GroupSqlalh:
    def __init__(self):
        pass

    @staticmethod
    def ins_sql(name, nums, remarks):
        sql = t_group(name=name, nums=nums, remarks=remarks)
        db.session.add(sql)
        db.session.commit()


class AccGroupList:
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
            return jsonify({"acc_group_list_msg": 'select list msg error'})

    @property
    def group_list_all(self):
        try:
            query_msg = t_group.query.all()
            list_msg = self.lt.dict_ls_reset_dict_auto(query_msg)
            len_msg = t_group.query.count()
            return jsonify({"host_status": 0,
                            "group_list_msg": list_msg,
                            "msg": "",
                            "group_len_msg": len_msg})
        except IOError:
            return jsonify({"host_list_msg": 'select list msg error',
                            "host_len_msg": 0})


class AccGroupDel:
    def __init__(self):
        self.id = request.values.get('id')

    @property
    def host_del(self):
        user_chk = t_group.query.filter_by(id=self.id).first()
        if not user_chk is None:
            db.session.delete(user_chk)
            db.session.commit()
            return jsonify({'group_del_status': 'true'})
        else:
            return jsonify({'group_del_status': 'fail'})


class AccGroupAdd:
    def __init__(self):
        self.name = request.values.get('name')
        self.nums = request.values.get('nums')
        self.remarks = request.values.get('remarks', type=str, default=None)
        self.host_sqlalh = GroupSqlalh()
        self.basesec = BaseSec()

    @property
    def host_add(self):
        try:
            user_chk = t_group.query.filter_by(name=self.name).first()
            if user_chk is None:
                self.host_sqlalh.ins_sql(self.name, self.nums, self.remarks)
                return jsonify({'acc_group_add_status': 'true'})
            else:
                return jsonify({'acc_group_add_status': 'sel_fail'})
        except IOError:
            return jsonify({'acc_group_add_status': 'con_fail'})
        except Exception:
            return jsonify({'acc_group_add_status': 'fail'})


class AccGroupUpdate(AccGroupAdd):
    def __init__(self):
        super(AccGroupUpdate, self).__init__()
        self.id = request.values.get('id')

    @property
    def update(self):
        try:
            t_group.query.filter_by(id=self.id).update({'name': self.name, 'nums': self.nums, 'remarks': self.remarks})
            db.session.commit()
            return jsonify({'acc_group_ping_status': 'true',
                            'acc_group_into_update': 'true'})
        except Exception:
            return jsonify({'acc_group_into_update': 'fail'})