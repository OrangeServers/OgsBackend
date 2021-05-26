import random, string, time
from flask import request, jsonify, session
from app.tools.redisdb import ConnRedis
from app.tools.sendmail import SendMail
from app.tools.basesec import BaseSec
from app.tools.SqlListTool import ListTool
from app.sqldb.SqlAlchemyConf import DBSession, User
from app.sqldb.SqlAlchemyDB import User2, t_acc_user, t_login_log, db, t_acc_group
from app.sqldb.SqlAlchemyInsert import LoginLogSqlalh
from app.conf.conf_test import MAIL_CONF, REDIS_CONF


class User_Sqlalh:
    def __init__(self):
        self.session = DBSession()

    def ins_sql(self, name, password, mail):
        sql = User(name=name, password=password, mail=mail)
        self.session.add(sql)
        self.session.commit()
        self.session.close()


class User2Sqlalh:
    def __init__(self):
        pass

    @staticmethod
    def ins_sql(name, password, mail):
        sql = User2(name=name, password=password, mail=mail)
        db.session.add(sql)
        db.session.commit()


class User_List:
    def __init__(self):
        self.lt = ListTool()

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
            return jsonify({"host_list_msg": 'select list msg error',
                            "host_len_msg": 0})


class LoginLogs:
    def __init__(self):
        self.lt = ListTool()
        self.table_page = request.values.get('page')
        self.table_limit = request.values.get('limit')
        self.table_offset = (int(self.table_page) - 1) * 10

    def get_login_logs(self):
        try:
            query_msg = t_login_log.query.offset(self.table_offset).limit(self.table_limit).all()
            list_msg = self.lt.time_ls_dict_que(query_msg, 'id', 'login_time')
            len_msg = t_login_log.query.count()
            return jsonify({"host_status": 0,
                            "login_list_msg": list_msg,
                            "msg": "",
                            "login_len_msg": len_msg})
        except IOError:
            return jsonify({"login_list_msg": 'select list msg error',
                            "login_len_msg": 0})

    def get_select_logs(self):
        login_jg_date = request.values.get('login_jg_date')
        try:
            query_msg = t_login_log.query.filter(t_login_log.login_name.like("%{}%".format(login_jg_date))).offset(self.table_offset).limit(self.table_limit).all()
            list_msg = self.lt.time_ls_dict_que(query_msg, 'id', 'login_time')
            len_msg = t_login_log.query.filter(t_login_log.login_name.like("%{}%".format(login_jg_date))).count()
            return jsonify({"host_status": 0,
                            "login_list_msg": list_msg,
                            "msg": "",
                            "login_len_msg": len_msg})
        except IOError:
            return jsonify({"login_list_msg": 'select list msg error',
                            "login_len_msg": 0})

    def get_date_logs(self):
        login_jg_date = request.values.get('login_jg_date')
        type(login_jg_date)
        msg = login_jg_date.split(' - ')
        try:
            query_msg = t_login_log.query.filter(t_login_log.login_time >= msg[0]).filter(
                t_login_log.login_time <= msg[1]).order_by(t_login_log.login_time.desc()).offset(
                self.table_offset).limit(self.table_limit).all()
            list_msg = self.lt.time_ls_dict_que(query_msg, 'id', 'login_time')
            len_msg = t_login_log.query.filter(t_login_log.login_time >= msg[0]).filter(
                t_login_log.login_time <= msg[1]).order_by(t_login_log.login_time.desc()).count()
            return jsonify({"host_status": 0,
                            "login_list_msg": list_msg,
                            "msg": "",
                            "login_len_msg": len_msg})
        except IOError:
            return jsonify({"login_list_msg": 'select list msg error',
                            "login_len_msg": 0})


class CheckMail:
    def __init__(self):
        self.session = DBSession()
        self.email = request.values.get('email')
        self.sendmail = SendMail(MAIL_CONF['form_mail'], MAIL_CONF['password'], MAIL_CONF['smtp_server'])
        self.cnres = ConnRedis(REDIS_CONF['host'], REDIS_CONF['port'])

    def send(self):
        # mail_chk = self.session.query(User).filter_by(mail=self.email).first()
        mail_chk = User2.query.filter_by(mail=self.email).first()
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
        self.session = DBSession()
        self.username = request.values.get('username')
        self.user_sqlalh = User_Sqlalh()
        self.user2_sqlalh = User2Sqlalh()

    def check(self):
        # user_chk = self.session.query(User).filter_by(name=self.username).first()
        user_chk = User2.query.filter_by(name=self.username).first()
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
        user_info = User2.query.filter_by(name=self.username).first()
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

    def register(self):
        # user_chk = self.session.query(User).filter_by(name=self.username)
        # mail_chk = self.session.query(User).filter_by(mail=self.email)
        user_chk = User2.query.filter_by(name=self.username)
        mail_chk = User2.query.filter_by(mail=self.email)
        if not user_chk is None:
            if not mail_chk is None:
                if not self.cnres.get_red(self.email) is None:
                    if self.verification == self.cnres.get_red(self.email):
                        # self.user_sqlalh.ins_sql(self.username, self.base.base_en(self.password), self.email)
                        self.user2_sqlalh.ins_sql(self.username, self.base.base_en(self.password), self.email)
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
