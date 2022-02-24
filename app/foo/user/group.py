import time, re
from flask import request, jsonify
from app.tools.basesec import BaseSec
from app.tools.SqlListTool import ListTool
from app.sqldb.SqlAlchemyDB import t_acc_group, t_auth_host, t_acc_user, db
from app.sqldb.SqlAlchemyInsert import AccGroupSqlalh, CzLogSqlalh
from app.tools.redisdb import ConnRedis, REDIS_CONF


class AccGroupList:
    def __init__(self):
        self.lt = ListTool()

    @property
    def group_list(self):
        try:
            group_id = request.values.get("id")
            query_msg = t_acc_group.query.filter_by(id=group_id).first()
            list_msg = self.lt.dict_reset_pop_auto(query_msg)
            list_msg.update({'code': 0})
            return jsonify(list_msg)
        except IOError:
            return jsonify({"code": 201})

    @property
    def group_name_list(self):
        try:
            que_auth_group = t_acc_group.query.with_entities(t_acc_group.name).all()
            group_list = self.lt.list_gather(que_auth_group)
            return jsonify({'code': 0, 'group_name_list_msg': group_list})
        except IOError:
            return jsonify({'code': 201})

    @property
    def group_list_all(self):
        try:
            table_page = request.values.get('page')
            table_limit = request.values.get('limit')
            table_offset = (int(table_page) - 1) * 10
            query_msg = t_acc_group.query.offset(table_offset).limit(table_limit).all()
            list_msg = self.lt.dict_ls_reset_dict_auto(query_msg)
            len_msg = t_acc_group.query.count()
            return jsonify({"code": 0,
                            "group_list_msg": list_msg,
                            "msg": "",
                            "group_len_msg": len_msg})
        except IOError:
            return jsonify({"host_list_msg": 'select list msg error',
                            "host_len_msg": 0})


class AccGroupAuto:
    def __init__(self):
        self.lt = ListTool()

    def grp_auth_auto_update(self):
        try:
            query_msg = self.lt.list_gather(t_acc_group.query.with_entities(t_acc_group.name).all())
            grp_msg = ','.join(query_msg)
            t_auth_host.query.filter_by(name='所有权限').update({'user_group': grp_msg})
            return True
        except IOError:
            return False


class AccGroupDel:
    def __init__(self):
        self.id = request.values.get('id')
        # 新增记录日志相关
        self.ords = ConnRedis(REDIS_CONF['host'], REDIS_CONF['port'])
        self.user_token = request.cookies.get('ogs_token')
        self.cz_name = self.ords.conn.get(self.user_token)
        self.new_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.cz_ins = CzLogSqlalh()
        self.grp_auto = AccGroupAuto()

    @property
    def host_del(self):
        user_chk = t_acc_group.query.filter_by(id=self.id).first()
        if user_chk:
            acc_user = t_acc_user.query.filter_by(group=user_chk.name).all()
            db.session.delete(user_chk)
            db.session.commit()
            for i in acc_user:
                db.session.delete(i)
                db.session.commit()
            self.cz_ins.ins_sql(self.cz_name, '用户组操作', '删除用户组', self.id, '成功', None, self.new_date)
            self.grp_auto.grp_auth_auto_update()
            return jsonify({'code': 0})
        else:
            self.cz_ins.ins_sql(self.cz_name, '用户组操作', '删除用户组', self.id, '失败', '系统内没有该用户组', self.new_date)
            return jsonify({'code': 111})


class AccGroupAdd:
    def __init__(self):
        self.name = request.values.get('name')
        self.remarks = request.values.get('remarks', type=str, default=None)
        self.host_sqlalh = AccGroupSqlalh()
        self.basesec = BaseSec()
        # 新增记录日志相关
        self.ords = ConnRedis(REDIS_CONF['host'], REDIS_CONF['port'])
        self.user_token = request.cookies.get('ogs_token')
        self.cz_name = self.ords.conn.get(self.user_token)
        self.new_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.cz_ins = CzLogSqlalh()
        self.grp_auto = AccGroupAuto()

    @property
    def host_add(self):
        try:
            user_chk = t_acc_group.query.filter_by(name=self.name).first()
            if user_chk is None:
                self.host_sqlalh.ins_sql(self.name, self.remarks)
                self.cz_ins.ins_sql(self.cz_name, '用户组操作', '新增用户组', self.name, '成功', None, self.new_date)
                self.grp_auto.grp_auth_auto_update()
                return jsonify({'code': 0})
            else:
                self.cz_ins.ins_sql(self.cz_name, '用户组操作', '新增用户组', self.name, '失败', '该用户组已存在', self.new_date)
                return jsonify({'code': 111})
        except IOError:
            self.cz_ins.ins_sql(self.cz_name, '用户组操作', '新增用户组', self.name, '失败', '连接数据库错误', self.new_date)
            return jsonify({'code': 201})
        except Exception:
            self.cz_ins.ins_sql(self.cz_name, '用户组操作', '新增用户组', self.name, '失败', '未知错误', self.new_date)
            return jsonify({'code': 2})


class AccGroupUpdate(AccGroupAdd):
    def __init__(self):
        super(AccGroupUpdate, self).__init__()
        self.id = request.values.get('id')

    @property
    def update(self):
        try:
            old_group = t_acc_group.query.filter_by(id=self.id).first()
            g_host = t_acc_user.query.filter_by(group=old_group.name).all()
            g_auth = t_auth_host.query.filter(t_auth_host.user_group.like("%{}%".format(old_group.name))).all()
            if g_host and self.name != old_group.name:
                for i in g_host:
                    t_acc_user.query.filter_by(id=i.id).update({'group': self.name})
                for x in g_auth:
                    if x.name != '所有权限':
                        g_auth_name = re.sub(old_group.name, self.name, x.user_group)
                        t_auth_host.query.filter_by(id=x.id).update({'user_group': g_auth_name})
            self.cz_ins.ins_sql(self.cz_name, '用户组操作', '修改用户组', self.name, '成功', None, self.new_date)
            t_acc_group.query.filter_by(id=self.id).update(
                {'name': self.name, 'remarks': self.remarks})
            db.session.commit()
            self.grp_auto.grp_auth_auto_update()
            return jsonify({'code': 0})
        except Exception as e:
            print(e)
            self.cz_ins.ins_sql(self.cz_name, '用户组操作', '修改用户组', self.name, '失败', '连接数据库错误', self.new_date)
            return jsonify({'code': 2})
