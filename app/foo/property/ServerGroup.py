import time, re
from flask import request, jsonify
from app.tools.basesec import BaseSec
from app.tools.SqlListTool import ListTool
from app.sqldb.SqlAlchemyDB import t_group, t_auth_host, t_host, db
from app.sqldb.SqlAlchemyInsert import GroupSqlalh, CzLogSqlalh
from app.tools.redisdb import ConnRedis, REDIS_CONF
from app.tools.at import auth_list_get


class ServerGroupList:
    def __init__(self):
        self.lt = ListTool()
        self.ords = ConnRedis(REDIS_CONF['host'], REDIS_CONF['port'])

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
        user_token = request.cookies.get('ogs_token')
        name = self.ords.conn.get(user_token)
        try:
            que_auth_group = t_auth_host.query.filter(t_auth_host.user.like("%{}%".format(name))).all()
            auth_group = self.lt.auth_ls_list_que(que_auth_group)
            group_list = list(auth_group)
            return jsonify({'code': 0, 'group_name_list_msg': group_list})
        except AttributeError:
            return jsonify({"code": 0,
                            "group_list_msg": '',
                            "msg": "",
                            "group_len_msg": 0})
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
        except AttributeError:
            return jsonify({"code": 0,
                            "group_list_msg": '',
                            "msg": "",
                            "group_len_msg": 0})
        except IOError:
            return jsonify({"code": 201})


class ServerGroupAuto:
    def __init__(self):
        self.lt = ListTool()

    def grp_auth_auto_update(self):
        try:
            query_msg = self.lt.list_gather(t_group.query.with_entities(t_group.name).all())
            grp_msg = ','.join(query_msg)
            t_auth_host.query.filter_by(name='????????????').update({'host_group': grp_msg})
            return True
        except IOError:
            return False


class ServerGroupDel:
    def __init__(self):
        self.id = request.values.get('id')
        # ????????????????????????
        self.ords = ConnRedis(REDIS_CONF['host'], REDIS_CONF['port'])
        self.user_token = request.cookies.get('ogs_token')
        self.cz_name = self.ords.conn.get(self.user_token)
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
            self.cz_ins.ins_sql(self.cz_name, '???????????????', '???????????????', self.id, '??????', None, self.new_date)
            self.grp_auto.grp_auth_auto_update()
            return jsonify({'code': 0})
        else:
            self.cz_ins.ins_sql(self.cz_name, '???????????????', '???????????????', self.id, '??????', '???????????????????????????', self.new_date)
            return jsonify({'code': 111})


class ServerGroupAdd:
    def __init__(self):
        self.name = request.values.get('name')
        self.remarks = request.values.get('remarks', type=str, default=None)
        self.host_sqlalh = GroupSqlalh()
        self.basesec = BaseSec()
        # ????????????????????????
        self.ords = ConnRedis(REDIS_CONF['host'], REDIS_CONF['port'])
        self.user_token = request.cookies.get('ogs_token')
        self.cz_name = self.ords.conn.get(self.user_token)
        self.new_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.cz_ins = CzLogSqlalh()
        self.grp_auto = ServerGroupAuto()

    @property
    def host_add(self):
        try:
            user_chk = t_group.query.filter_by(name=self.name).first()
            if user_chk is None:
                self.host_sqlalh.ins_sql(self.name, self.remarks)
                self.cz_ins.ins_sql(self.cz_name, '???????????????', '???????????????', self.name, '??????', None, self.new_date)
                self.grp_auto.grp_auth_auto_update()
                return jsonify({'code': 0})
            else:
                self.cz_ins.ins_sql(self.cz_name, '???????????????', '???????????????', self.name, '??????', '?????????????????????', self.new_date)
                return jsonify({'code': 111})
        except IOError:
            self.cz_ins.ins_sql(self.cz_name, '???????????????', '???????????????', self.name, '??????', '?????????????????????', self.new_date)
            return jsonify({'code': 201})
        except Exception:
            self.cz_ins.ins_sql(self.cz_name, '???????????????', '???????????????', self.name, '??????', '????????????', self.new_date)
            return jsonify({'code': 2})


class ServerGroupUpdate(ServerGroupAdd):
    def __init__(self):
        super(ServerGroupUpdate, self).__init__()
        self.id = request.values.get('id')
        self.nums = request.values.get('nums')

    @property
    def update(self):
        try:
            old_group = t_group.query.filter_by(id=self.id).first()
            g_host = t_host.query.filter_by(group=old_group.name).all()
            g_auth = t_auth_host.query.filter(t_auth_host.host_group.like("%{}%".format(old_group.name))).all()
            if g_host and self.name != old_group.name:
                for i in g_host:
                    t_host.query.filter_by(id=i.id).update({'group': self.name})
                for x in g_auth:
                    if x.name != '????????????':
                        g_auth_name = re.sub(old_group.name, self.name, x.host_group)
                        t_auth_host.query.filter_by(id=x.id).update({'host_group': g_auth_name})
            t_group.query.filter_by(id=self.id).update({'name': self.name, 'nums': self.nums, 'remarks': self.remarks})
            db.session.commit()
            self.cz_ins.ins_sql(self.cz_name, '???????????????', '???????????????', self.name, '??????', None, self.new_date)
            self.grp_auto.grp_auth_auto_update()
            return jsonify({'code': 0})
        except Exception as e:
            print(e)
            self.cz_ins.ins_sql(self.cz_name, '???????????????', '???????????????', self.name, '??????', '?????????????????????', self.new_date)
            return jsonify({'code': 2})
