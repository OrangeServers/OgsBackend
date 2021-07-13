import time
from flask import request, jsonify
from app.tools.basesec import BaseSec
from app.tools.SqlListTool import ListTool
from app.sqldb.SqlAlchemyDB import t_acc_group, t_cz_log, db
from app.sqldb.SqlAlchemyInsert import AccUserSqlalh, CzLogSqlalh


class AccGroupList:
    def __init__(self):
        self.lt = ListTool()

    @property
    def group_list(self):
        try:
            group_id = request.values.get("id")
            query_msg = t_acc_group.query.filter_by(id=group_id).first()
            list_msg = self.lt.dict_reset_pop_auto(query_msg)
            return jsonify(list_msg)
        except IOError:
            return jsonify({"acc_group_list_msg": 'select list msg error'})

    @property
    def group_list_all(self):
        try:
            table_page = request.values.get('page')
            table_limit = request.values.get('limit')
            table_offset = (int(table_page) - 1) * 10
            query_msg = t_acc_group.query.offset(table_offset).limit(table_limit).all()
            list_msg = self.lt.dict_ls_reset_dict_auto(query_msg)
            len_msg = t_acc_group.query.count()
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
        # 新增记录日志相关
        self.cz_name = request.values.get('cz_name')
        self.new_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.cz_ins = CzLogSqlalh()

    @property
    def host_del(self):
        user_chk = t_acc_group.query.filter_by(id=self.id).first()
        if user_chk:
            db.session.delete(user_chk)
            db.session.commit()
            self.cz_ins.ins_sql(self.cz_name, '用户组操作', '删除用户组', self.id, '成功', None, self.new_date)
            return jsonify({'acc_group_del_status': 'true'})
        else:
            self.cz_ins.ins_sql(self.cz_name, '用户组操作', '删除用户组', self.id, '失败', '系统内没有该用户组', self.new_date)
            return jsonify({'acc_group_del_status': 'fail'})


class AccGroupAdd:
    def __init__(self):
        self.name = request.values.get('name')
        self.remarks = request.values.get('remarks', type=str, default=None)
        self.host_sqlalh = AccUserSqlalh()
        self.basesec = BaseSec()
        # 新增记录日志相关
        self.cz_name = request.values.get('cz_name')
        self.new_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.cz_ins = CzLogSqlalh()

    @property
    def host_add(self):
        try:
            user_chk = t_acc_group.query.filter_by(name=self.name).first()
            if user_chk is None:
                self.host_sqlalh.ins_sql(self.name, self.remarks)
                self.cz_ins.ins_sql(self.cz_name, '用户组操作', '新增用户组', self.name, '成功', None, self.new_date)
                return jsonify({'acc_group_add_status': 'true'})
            else:
                self.cz_ins.ins_sql(self.cz_name, '用户组操作', '新增用户组', self.name, '失败', '该用户组已存在', self.new_date)
                return jsonify({'acc_group_add_status': 'sel_fail'})
        except IOError:
            self.cz_ins.ins_sql(self.cz_name, '用户组操作', '新增用户组', self.name, '失败', '连接数据库错误', self.new_date)
            return jsonify({'acc_group_add_status': 'con_fail'})
        except Exception:
            self.cz_ins.ins_sql(self.cz_name, '用户组操作', '新增用户组', self.name, '失败', '未知错误', self.new_date)
            return jsonify({'acc_group_add_status': 'fail'})


class AccGroupUpdate(AccGroupAdd):
    def __init__(self):
        super(AccGroupUpdate, self).__init__()
        self.id = request.values.get('id')

    @property
    def update(self):
        try:
            self.cz_ins.ins_sql(self.cz_name, '用户组操作', '修改用户组', self.name, '成功', None, self.new_date)
            t_acc_group.query.filter_by(id=self.id).update(
                {'name': self.name, 'nums': self.nums, 'remarks': self.remarks})
            db.session.commit()
            return jsonify({'acc_group_ping_status': 'true',
                            'acc_group_into_update': 'true'})
        except Exception:
            self.cz_ins.ins_sql(self.cz_name, '用户组操作', '修改用户组', self.name, '失败', '连接数据库错误', self.new_date)
            return jsonify({'acc_group_into_update': 'fail'})
