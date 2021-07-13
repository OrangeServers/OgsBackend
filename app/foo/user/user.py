import random, string, time
from flask import request, jsonify, session
from app.tools.basesec import BaseSec
from app.tools.SqlListTool import ListTool
from app.tools.sendmail import SendMail
from app.tools.redisdb import ConnRedis
from app.sqldb.SqlAlchemyDB import t_acc_user, t_cz_log, db
from app.sqldb.SqlAlchemyInsert import AccUserSqlalh, LoginLogSqlalh, CzLogSqlalh
from app.conf.conf_test import REDIS_CONF, MAIL_CONF


class AccUserList:
    def __init__(self):
        self.lt = ListTool()
        self.cnres = ConnRedis(REDIS_CONF['host'], REDIS_CONF['port'])

    @property
    def acc_user_list(self):
        try:
            acc_user_type = request.values.get('user_type')
            if acc_user_type == 'user_list':
                acc_user_id = request.values.get("id")
                query_msg = t_acc_user.query.filter_by(id=acc_user_id).first()
                list_msg = self.lt.dict_reset_pop_auto(query_msg, 'password')
                return jsonify(list_msg)
            elif acc_user_type == 'user_info':
                acc_user_name = request.values.get("name")
                query_msg = t_acc_user.query.filter_by(name=acc_user_name).first()
                list_msg = self.lt.dict_reset_pop_auto(query_msg, 'password')
                return jsonify(list_msg)
        except IOError:
            return jsonify({"acc_user_list_msg": 'select list msg error'})

    @property
    def acc_user_auth_list(self):
        try:
            acc_user_name = request.values.get("name")
            user_role = acc_user_name + '_role'
            role = self.cnres.get_red(user_role)
            return jsonify({'usrole': role})
        except IOError:
            return jsonify({"acc_user_list_msg": 'select list msg error'})
        except TypeError:
            return jsonify({"acc_user_list_msg": 'name is none error'})

    @property
    def acc_user_list_all(self):
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


class CheckMail:
    def __init__(self):
        self.email = request.values.get('email')
        self.sendmail = SendMail(MAIL_CONF['form_mail'], MAIL_CONF['password'], MAIL_CONF['smtp_server'])
        self.cnres = ConnRedis(REDIS_CONF['host'], REDIS_CONF['port'])

    def send(self):
        mail_chk = t_acc_user.query.filter_by(mail=self.email).first()
        if not mail_chk:
            mail_verification = ''.join(random.sample(string.digits, 4))
            msg = ("您在OrangeServer上注册账号的的验证码是   %s   验证码有效期3分钟，请在3分钟内完成注册" % mail_verification)
            self.cnres.set_red(self.email, mail_verification)
            self.cnres.exp_red(self.email, 180)
            self.sendmail.send(self.email, 'OrangeServer', '注册验证码', msg)
            return jsonify({'send_status': 'true'})
        else:
            return jsonify({'send_status': 'fail'})


class CheckUser:
    def __init__(self):
        self.username = request.values.get('username')

    def check(self):
        user_chk = t_acc_user.query.filter_by(name=self.username).first()
        if user_chk:
            return jsonify({'chk_user_status': 'fail'})
        else:
            return jsonify({'chk_user_status': 'true'})


class UserLogin(CheckUser):
    def __init__(self):
        super(UserLogin, self).__init__()
        self.password = request.values.get('password')
        self.user_nw_ip = request.headers.get('X-Real-IP')
        self.user_agent = request.headers.get('User-Agent')
        self.new_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.base = BaseSec()
        self.login_ins = LoginLogSqlalh

        self.cnres = ConnRedis(REDIS_CONF['host'], REDIS_CONF['port'])

    def login_dl(self):
        user_info = t_acc_user.query.filter_by(name=self.username).first()
        user_gw_ip = request.values.get('user_gw_ip')
        user_gw_cs = request.values.get('user_gw_cs')
        if not user_info is None:
            password_de = self.base.base_de(user_info.password)
            if self.username == user_info.name and self.password == password_de:
                # 每个用户登录生成一个session
                # session["user"] = self.username
                query_user_role = t_acc_user.query.filter_by(name=self.username).first()
                user_role = query_user_role.__dict__
                role_name = self.username + '_role'
                self.cnres.set_red(role_name, user_role['usrole'])
                self.login_ins.ins_sql(self.username, self.user_nw_ip, user_gw_ip, user_gw_cs, self.user_agent, '成功',
                                       None, self.new_date)
                return jsonify({'chk_status': 'true'})
            else:
                self.login_ins.ins_sql(self.username, self.user_nw_ip, user_gw_ip, user_gw_cs, self.user_agent, '失败',
                                       '密码错误', self.new_date)
                return jsonify({'password_status': 'fail'})
        else:
            self.login_ins.ins_sql(self.username, self.user_nw_ip, user_gw_ip, user_gw_cs, self.user_agent, '失败',
                                   '用户名无效', self.new_date)
            return jsonify({'user_status': 'fail'})


class UserRegister(UserLogin):
    def __init__(self):
        super(UserRegister, self).__init__()
        self.email = request.values.get('email')
        self.verification = request.values.get('verification')
        self.cnres = ConnRedis(REDIS_CONF['host'], REDIS_CONF['port'])
        self.reg_ins = AccUserSqlalh

    def register(self):
        user_chk = t_acc_user.query.filter_by(name=self.username)
        mail_chk = t_acc_user.query.filter_by(mail=self.email)
        if not user_chk is None:
            if not mail_chk is None:
                if not self.cnres.get_red(self.email) is None:
                    if self.verification == self.cnres.get_red(self.email):
                        # self.user_sqlalh.ins_sql(self.username, self.base.base_en(self.password), self.email)
                        self.reg_ins.ins_sql(None, self.username, self.base.base_en(self.password), 'develop', self.email, None)
                        return jsonify({
                            'chk_user_status': 'true',
                            'verification': 'true',
                            'chk_mail_status': 'true'
                        })
                    else:
                        return jsonify({
                            'verification': 'fail',
                        })
                else:
                    return jsonify({'chk_verification': 'fail'})
            else:
                return jsonify({
                    'chk_user_status': 'true',
                    'chk_mail_status': 'fail'
                })
        else:
            return jsonify({'chk_user_status': 'fail'})


class AccUserDel:
    def __init__(self):
        # self.host_ip = request.values.get('host_ip')
        self.id = request.values.get('id')
        # 新增记录日志相关
        self.cz_name = request.values.get('cz_name')
        self.new_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.cz_ins = CzLogSqlalh()

    @property
    def host_del(self):
        # user_chk = Host.query.filter_by(host_ip=self.host_ip).first()
        user_chk = t_acc_user.query.filter_by(id=self.id).first()
        if user_chk:
            db.session.delete(user_chk)
            db.session.commit()
            self.cz_ins.ins_sql(self.cz_name, '用户修改', '删除用户', self.id, '成功', None, self.new_date)
            return jsonify({'acc_user_del_status': 'true'})
        else:
            self.cz_ins.ins_sql(self.cz_name, '用户修改', '删除用户', self.id, '失败', '系统内没有该用户', self.new_date)
            return jsonify({'acc_user_del_status': 'fail'})


class AccUserAdd:
    def __init__(self):
        self.alias = request.values.get('alias')
        self.name = request.values.get('name')
        self.password = request.values.get('password')
        self.usrole = request.values.get('usrole')
        self.mail = request.values.get('mail')
        self.remarks = request.values.get('remarks', type=str, default=None)
        self.user_ins = AccUserSqlalh()
        self.basesec = BaseSec()
        # 新增记录日志相关
        self.cz_name = request.values.get('cz_name')
        self.new_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.cz_ins = CzLogSqlalh()

    @property
    def host_add(self):
        try:
            user_chk = t_acc_user.query.filter_by(name=self.name).first()
            if user_chk is None:
                password_en = self.basesec.base_en(self.password)
                self.user_ins.ins_sql(self.alias, self.name, password_en, self.usrole, self.mail,
                                         self.remarks)
                self.cz_ins.ins_sql(self.cz_name, '用户修改', '新增用户', self.name, '成功', None, self.new_date)
                return jsonify({'acc_user_add_status': 'true'})
            else:
                self.cz_ins.ins_sql(self.cz_name, '用户修改', '新增用户', self.name, '失败', '该用户已存在', self.new_date)
                return jsonify({'acc_user_add_status': 'sel_fail'})
        except IOError:
            self.cz_ins.ins_sql(self.cz_name, '用户修改', '新增用户', self.name, '失败', '连接数据库错误', self.new_date)
            return jsonify({'acc_user_add_status': 'con_fail'})
        except Exception:
            self.cz_ins.ins_sql(self.cz_name, '用户修改', '新增用户', self.name, '失败', '未知错误', self.new_date)
            return jsonify({'acc_user_add_status': 'fail'})


class AccUserUpdate(AccUserAdd):
    def __init__(self):
        super(AccUserUpdate, self).__init__()
        self.id = request.values.get('id')
        self.cnres = ConnRedis(REDIS_CONF['host'], REDIS_CONF['port'])

    @property
    def update(self):
        try:
            password_en = self.basesec.base_en(self.password)
            t_acc_user.query.filter_by(id=self.id).update({'alias': self.alias, 'name': self.name,
                                                           'password': password_en,
                                                           'usrole': self.usrole,
                                                           'mail': self.mail, 'remarks': self.remarks})
            db.session.commit()
            role_name = self.name + '_role'
            self.cnres.set_red(role_name, self.usrole)
            self.cz_ins.ins_sql(self.cz_name, '用户修改', '变更用户', self.name, '成功', None, self.new_date)
            return jsonify({'acc_user_ping_status': 'true',
                            'acc_user_into_update': 'true'})
        except Exception:
            self.cz_ins.ins_sql(self.cz_name, '用户修改', '变更用户', self.name, '失败', '连接数据库错误', self.new_date)
            return jsonify({'acc_user_into_update': 'fail'})