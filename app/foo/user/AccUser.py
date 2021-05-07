import random, string
from flask import request, jsonify, session
from app.tools.redisdb import ConnRedis
from app.tools.sendmail import SendMail
from app.tools.basesec import BaseSec
from app.tools.SqlListTool import ListTool
from app.sqldb.SqlAlchemyConf import DBSession, User
from app.sqldb.SqlAlchemyDB import User2, t_acc_user, db
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
        self.base = BaseSec()

    def login_dl(self):
        # user_info = self.session.query(User).filter_by(name=self.username).first()
        user_info = User2.query.filter_by(name=self.username).first()
        if not user_info is None:
            password_de = self.base.base_de(user_info.password)
            if self.username == user_info.name and self.password == password_de:
                # 每个用户登录生成一个session
                # session["user"] = self.username
                return jsonify({'chk_status': 'true'})
            else:
                return jsonify({'password_status': 'fail'})
        else:
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
