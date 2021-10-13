import os
import stat
import time
from flask import request, jsonify
from app.sqldb.SqlAlchemyDB import t_sys_user, t_auth_host, t_acc_user, db
from app.sqldb.SqlAlchemyInsert import SysUserSqlalh, CzLogSqlalh
from app.tools.SqlListTool import ListTool
from app.tools.basesec import BaseSec
from app.conf.conf_test import FILE_CONF


class SysUserList:
    def __init__(self):
        self.ls_tool = ListTool()

    @property
    def sys_user_name_list(self):
        try:
            # 还差根据用户组选出系统用户名
            name = request.values.get('name')

            user_name_list = t_auth_host.query.filter(t_auth_host.user.like("%{}%".format(name))).all()
            grp_name = t_acc_user.query.filter_by(name=name).first()
            user_gre_list = t_auth_host.query.filter(t_auth_host.user_group.like("%{}%".format(grp_name.group))).all()

            def sys_list_get(msg_list):
                sys_list = []
                for i in msg_list:
                    sys_user_list = i.sys_user
                    if sys_user_list:
                        sys_user = sys_user_list.split(',')
                        sys_list.append(sys_user)
                return list(set(self.ls_tool.list_gather(sys_list)))

            name_list = list(set(sys_list_get(user_name_list) + sys_list_get(user_gre_list)))
            return jsonify({'msg': name_list})
        except IOError:
            return jsonify({"sys_user_list_msg": 'select list msg error'})

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
            table_page = request.values.get('page')
            table_limit = request.values.get('limit')
            table_offset = (int(table_page) - 1) * 10
            query_msg = t_sys_user.query.offset(table_offset).limit(table_limit).all()
            list_msg = self.ls_tool.dict_ls_reset_dict_auto(query_msg, 'host_password')
            len_msg = t_sys_user.query.count()
            return jsonify({"host_status": 0,
                            "sys_user_list_msg": list_msg,
                            "msg": "",
                            "sys_user_len_msg": len_msg})
        except IOError:
            return jsonify({"sys_user_list_msg": 'select list msg error',
                            "sys_user_len_msg": 0})


class SysUserAuto:
    def __init__(self):
        self.lt = ListTool()

    def user_auth_auto_update(self):
        try:
            query_msg = self.lt.list_gather(t_sys_user.query.with_entities(t_sys_user.alias).all())
            user_msg = ','.join(query_msg)
            t_auth_host.query.filter_by(name='所有权限').update({'sys_user': user_msg})
            return True
        except IOError:
            return False


class SysUserDel:
    def __init__(self):
        # self.host_ip = request.values.get('host_ip')
        self.id = request.values.get('id')
        # 新增记录日志相关
        self.cz_name = request.values.get('cz_name')
        self.new_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.cz_ins = CzLogSqlalh()
        self.user_auto = SysUserAuto()

    @property
    def host_del(self):
        # user_chk = Host.query.filter_by(host_ip=self.host_ip).first()
        user_chk = t_sys_user.query.filter_by(id=self.id).first()
        if user_chk:
            if user_chk.host_key:
                os.remove(FILE_CONF['key_path'] + user_chk.alias + '_rsa')
            db.session.delete(user_chk)
            db.session.commit()
            self.cz_ins.ins_sql(self.cz_name, '资产用户操作', '删除资产用户', self.id, '成功', None, self.new_date)
            self.user_auto.user_auth_auto_update()
            return jsonify({'sys_user_del_status': 'true'})
        else:
            self.cz_ins.ins_sql(self.cz_name, '资产用户操作', '删除资产用户', self.id, '失败', '系统内没有该用户', self.new_date)
            return jsonify({'sys_user_del_status': 'fail'})


class SysUserAdd:
    def __init__(self):
        self.alias = request.values.get('alias')
        self.host_user = request.values.get('host_user')
        self.host_password = request.values.get('host_password', default=None)
        # 新增获取传入的key文件
        self.host_key = request.files.get('host_key')

        self.agreement = request.values.get('agreement')
        self.remarks = request.values.get('remarks', type=str, default=None)
        self.host_sqlalh = SysUserSqlalh()
        self.basesec = BaseSec()
        # 新增记录日志相关
        self.cz_name = request.values.get('cz_name')
        self.new_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.cz_ins = CzLogSqlalh()
        self.user_auto = SysUserAuto()

    @property
    def host_add(self):
        try:
            user_chk = t_sys_user.query.filter_by(alias=self.alias).first()
            if user_chk is None:
                # 保存key文件 判断文件是否存在，后续逻辑待优化
                if self.host_key:
                    key_path = FILE_CONF['key_path'] + self.alias + '_rsa'
                    self.host_key.save(key_path)
                    os.chmod(key_path, stat.S_IRUSR | stat.S_IWUSR)
                else:
                    key_path = None
                if self.host_password:
                    password_en = self.basesec.base_en(self.host_password)
                else:
                    password_en = None
                self.host_sqlalh.ins_sql(self.alias, self.host_user, password_en, key_path, self.agreement,
                                         self.remarks)
                self.cz_ins.ins_sql(self.cz_name, '资产用户操作', '新增资产用户', self.host_user, '成功', None, self.new_date)
                self.user_auto.user_auth_auto_update()
                return jsonify({'sys_user_add_status': 'true'})
            else:
                self.cz_ins.ins_sql(self.cz_name, '资产用户操作', '新增资产用户', self.host_user, '失败', '该资产用户已存在', self.new_date)
                return jsonify({'sys_user_add_status': 'sel_fail'})
        except IOError:
            self.cz_ins.ins_sql(self.cz_name, '资产用户操作', '新增资产用户', self.host_user, '失败', '连接数据库失败', self.new_date)
            return jsonify({'sys_user_add_status': 'con_fail'})
        except Exception:
            self.cz_ins.ins_sql(self.cz_name, '资产用户操作', '新增资产用户', self.host_user, '失败', '未知错误', self.new_date)
            return jsonify({'sys_user_add_status': 'fail'})


class SysUserUpdate(SysUserAdd):
    def __init__(self):
        super(SysUserUpdate, self).__init__()
        self.id = request.values.get('id')
        self.nums = request.values.get('nums')
        self.user_auto = SysUserAuto()

    @property
    def update(self):
        query_msg = t_sys_user.query.filter_by(id=self.id).first()
        try:
            if self.host_password:
                password_en = self.basesec.base_en(self.host_password)
            else:
                password_en = query_msg.host_password
            if self.host_key:
                key_path = FILE_CONF['key_path'] + self.alias + '_rsa'
                self.host_key.save(key_path)
                os.chmod(key_path, stat.S_IRUSR | stat.S_IWUSR)
            else:
                key_path = query_msg.host_key
            t_sys_user.query.filter_by(id=self.id).update({'alias': self.alias, 'host_user': self.host_user,
                                                           'host_password': password_en,
                                                           'agreement': self.agreement,
                                                           'host_key': key_path,
                                                           'nums': self.nums, 'remarks': self.remarks})
            db.session.commit()
            self.cz_ins.ins_sql(self.cz_name, '资产用户操作', '修改资产用户', self.host_user, '成功', None, self.new_date)
            self.user_auto.user_auth_auto_update()
            return jsonify({'sys_user_ping_status': 'true',
                            'sys_user_into_update': 'true'})
        except Exception:
            self.cz_ins.ins_sql(self.cz_name, '资产用户操作', '修改资产用户', self.host_user, '失败', '连接数据失败', self.new_date)
            return jsonify({'sys_user_into_update': 'fail'})
