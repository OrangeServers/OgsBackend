import time
from flask import request, jsonify
from app.tools.basesec import BaseSec
from app.tools.SqlListTool import ListTool
from app.sqldb.SqlAlchemyDB import t_group, t_auth_host, t_host, t_acc_user, db
from app.sqldb.SqlAlchemyInsert import GroupSqlalh, CzLogSqlalh
from app.tools.at import auth_list_get


class ServerGroupList:
    def __init__(self):
        self.lt = ListTool()

    @property
    def group_list(self):
        try:
            group_id = request.values.get("id")
            query_msg = t_group.query.filter_by(id=group_id).first()
            list_msg = self.lt.dict_reset_pop_auto(query_msg)
            list_msg.update({'code': 0})
            return jsonify(list_msg)
        except IOError:
            return jsonify({"code": 201})

    @property
    def group_name_list(self):
        name = request.values.get('name')
        try:
            que_auth_group = t_auth_host.query.filter(t_auth_host.user.like("%{}%".format(name))).all()
            auth_group = self.lt.auth_ls_list_que(que_auth_group)
            group_list = list(auth_group)
            return jsonify({'code': 0, 'group_name_list_msg': group_list})
        except IOError:
            return jsonify({'code': 201})

    @property
    def group_list_all(self):
        try:
            table_page = request.values.get('page')
            table_limit = request.values.get('limit')
            table_offset = (int(table_page) - 1) * 10
            auth_list = auth_list_get()
            query_msg = t_group.query.filter(t_group.name.in_(auth_list)).offset(table_offset).limit(table_limit).all()
            list_msg = self.lt.dict_ls_reset_dict_auto(query_msg)
            len_msg = t_group.query.filter(t_group.name.in_(auth_list)).count()
            return jsonify({"code": 0,
                            "group_list_msg": list_msg,
                            "msg": "",
                            "group_len_msg": len_msg})
        except IOError:
            return jsonify({"code": 201})


class ServerGroupAuto:
    def __init__(self):
        self.lt = ListTool()

    def grp_auth_auto_update(self):
        try:
            query_msg = self.lt.list_gather(t_group.query.with_entities(t_group.name).all())
            grp_msg = ','.join(query_msg)
            t_auth_host.query.filter_by(name='所有权限').update({'host_group': grp_msg})
            return True
        except IOError:
            return False


class ServerGroupDel:
    def __init__(self):
        self.id = request.values.get('id')
        # 新增记录日志相关
        self.cz_name = request.values.get('cz_name')
        self.new_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.cz_ins = CzLogSqlalh()
        self.grp_auto = ServerGroupAuto()

    @property
    def host_del(self):
        user_chk = t_group.query.filter_by(id=self.id).first()
        if user_chk:
            query_host = t_host.query.filter_by(group=user_chk.name).all()
            db.session.delete(user_chk)
            db.session.commit()
            for i in query_host:
                db.session.delete(i)
                db.session.commit()
            self.cz_ins.ins_sql(self.cz_name, '资产组操作', '删除资产组', self.id, '成功', None, self.new_date)
            self.grp_auto.grp_auth_auto_update()
            return jsonify({'code': 0})
        else:
            self.cz_ins.ins_sql(self.cz_name, '资产组操作', '删除资产组', self.id, '失败', '系统内没有该资产组', self.new_date)
            return jsonify({'code': 111})


class ServerGroupAdd:
    def __init__(self):
        self.name = request.values.get('name')
        self.remarks = request.values.get('remarks', type=str, default=None)
        self.host_sqlalh = GroupSqlalh()
        self.basesec = BaseSec()
        # 新增记录日志相关
        self.cz_name = request.values.get('cz_name')
        self.new_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.cz_ins = CzLogSqlalh()
        self.grp_auto = ServerGroupAuto()

    @property
    def host_add(self):
        try:
            user_chk = t_group.query.filter_by(name=self.name).first()
            if user_chk is None:
                self.host_sqlalh.ins_sql(self.name, self.remarks)
                self.cz_ins.ins_sql(self.cz_name, '资产组操作', '新增资产组', self.name, '成功', None, self.new_date)
                self.grp_auto.grp_auth_auto_update()
                return jsonify({'code': 0})
            else:
                self.cz_ins.ins_sql(self.cz_name, '资产组操作', '新增资产组', self.name, '失败', '该资产组已存在', self.new_date)
                return jsonify({'code': 111})
        except IOError:
            self.cz_ins.ins_sql(self.cz_name, '资产组操作', '新增资产组', self.name, '失败', '连接数据库失败', self.new_date)
            return jsonify({'code': 201})
        except Exception:
            self.cz_ins.ins_sql(self.cz_name, '资产组操作', '新增资产组', self.name, '失败', '未知错误', self.new_date)
            return jsonify({'code': 2})


class ServerGroupUpdate(ServerGroupAdd):
    def __init__(self):
        super(ServerGroupUpdate, self).__init__()
        self.id = request.values.get('id')
        self.nums = request.values.get('nums')

    @property
    def update(self):
        try:
            t_group.query.filter_by(id=self.id).update({'name': self.name, 'nums': self.nums, 'remarks': self.remarks})
            db.session.commit()
            self.cz_ins.ins_sql(self.cz_name, '资产组操作', '修改资产组', self.name, '成功', None, self.new_date)
            return jsonify({'code': 0})
        except Exception as e:
            print(e)
            self.cz_ins.ins_sql(self.cz_name, '资产组操作', '修改资产组', self.name, '失败', '连接数据库错误', self.new_date)
            return jsonify({'code': 2})
