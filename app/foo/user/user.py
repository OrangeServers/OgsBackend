import random, string, time, hashlib, os
from flask import request, jsonify, session
from app.tools.basesec import BaseSec
from app.tools.SqlListTool import ListTool
from app.tools.sendmail import SendMail
from app.tools.redisdb import ConnRedis
from app.sqldb.SqlAlchemyDB import t_acc_user, t_acc_group, t_settings, db
from app.sqldb.SqlAlchemyInsert import AccUserSqlalh, LoginLogSqlalh, CzLogSqlalh
from app.conf.conf import REDIS_CONF, MAIL_CONF
from app.tools.at import Log


class AccUserList:
    def __init__(self):
        self.lt = ListTool()
        self.ords = ConnRedis(REDIS_CONF['host'], REDIS_CONF['port'])

    @property
    def acc_user_alias(self):
        user_token = request.cookies.get('ogs_token')
        acc_user_name = self.ords.conn.get(user_token)
        # acc_user_name = request.values.get("name")
        log_msg = 'req_body: [ name=%s ] /account/user/alias' % acc_user_name
        try:
            user_alias = self.ords.conn.get(acc_user_name + '_alias')
            return jsonify({'alias': user_alias, 'username': acc_user_name})
        except IOError:
            Log.logger.info(log_msg + ' \"fail select list msg error\"')
            return jsonify({"acc_user_list_msg": 'select list msg error'})

    @property
    def acc_user_list(self):
        acc_user_type = request.values.get('user_type')
        log_msg = 'req_body: [ user_type=%s ] /account/user/list' % acc_user_type
        try:
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
            Log.logger.info(log_msg + ' \"fail select list msg error\"')
            return jsonify({"code": 201})

    @property
    def acc_user_auth_list(self):
        user_token = request.cookies.get('ogs_token')
        acc_user_name = self.ords.conn.get(user_token)
        log_msg = 'req_body: [ name=%s ] /account/user/auth_list' % acc_user_name
        try:
            user_role = acc_user_name + '_role'
            role = self.ords.conn.get(user_role)
            return jsonify({'code': 0, 'usrole': role})
        except IOError:
            Log.logger.info(log_msg + ' \"fail select list msg error\"')
            return jsonify({"code": 201})
        except TypeError:
            Log.logger.info(log_msg + ' \"fail name is none error\"')
            return jsonify({"code": 211})

    @property
    def acc_user_list_all(self):
        log_msg = 'req_body: [ None ] /account/user/list_all'
        table_page = request.values.get('page')
        table_limit = request.values.get('limit')
        table_offset = (int(table_page) - 1) * 10
        try:
            query_msg = t_acc_user.query.offset(table_offset).limit(table_limit).all()
            list_msg = self.lt.dict_ls_reset_dict_auto(query_msg, 'password')
            len_msg = t_acc_user.query.count()
            return jsonify({"code": 0,
                            "acc_user_list_msg": list_msg,
                            "msg": "",
                            "acc_user_len_msg": len_msg})
        except IOError:
            Log.logger.info(log_msg + ' \"fail select list msg error\"')
            return jsonify({'code': 201})


class CheckMail:
    def __init__(self):
        self.email = request.values.get('email')
        self.sendmail = SendMail(MAIL_CONF['form_mail'], MAIL_CONF['password'], MAIL_CONF['smtp_server'])
        self.ords = ConnRedis(REDIS_CONF['host'], REDIS_CONF['port'])

    def send(self):
        mail_chk = t_acc_user.query.filter_by(mail=self.email).first()
        log_msg = 'req_body: [ email=%s ] /mail/send_user_mail' % self.email
        if not mail_chk:
            mail_verification = ''.join(random.sample(string.digits, 4))
            msg = ("??????OrangeServer?????????????????????????????????   %s   ??????????????????3???????????????3?????????????????????" % mail_verification)
            self.ords.conn.set(self.email, mail_verification)
            self.ords.conn.expire(self.email, 180)
            self.sendmail.send(self.email, 'OrangeServer', '???????????????', msg)
            return jsonify({'code': 0})
        else:
            Log.logger.info(log_msg + ' \"fail\"')
            return jsonify({'code': 104})


class CheckUser:
    def __init__(self):
        self.username = request.values.get('username')

    def check(self):
        user_chk = t_acc_user.query.filter_by(name=self.username).first()
        log_msg = 'req_body: [ username=%s ] /account/chk_username' % self.username
        if user_chk:
            Log.logger.info(log_msg + ' \"fail\"')
            return jsonify({'code': 103})
        else:
            return jsonify({'code': 0})


class UserLogin(CheckUser):
    def __init__(self):
        super(UserLogin, self).__init__()
        self.password = request.values.get('password')
        self.user_nw_ip = request.headers.get('X-Real-IP')
        self.user_agent = request.headers.get('User-Agent')
        self.new_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.base = BaseSec()
        self.login_ins = LoginLogSqlalh

        self.ords = ConnRedis(REDIS_CONF['host'], REDIS_CONF['port'])

    def login_dl(self):
        log_msg = 'req_body: [ username=%s, password=%s ] /account/login_dl' % (self.username, self.password)
        user_info = t_acc_user.query.filter_by(name=self.username).first()
        user_gw_ip = request.values.get('user_gw_ip')
        user_gw_cs = request.values.get('user_gw_cs')
        if user_info is not None:
            password_de = self.base.base_de(user_info.password)
            if self.username == user_info.name and self.password == password_de:
                # ??????????????????????????????session
                # session["user"] = self.username
                query_user_role = t_acc_user.query.filter_by(name=self.username).first()
                user_role = query_user_role.__dict__
                role_name = self.username + '_role'
                self.ords.conn.set(role_name, user_role['usrole'])
                self.login_ins.ins_sql(self.username, self.user_nw_ip, user_gw_ip, user_gw_cs, self.user_agent, '??????',
                                       None, self.new_date)
                return jsonify({'code': 0})
            else:
                self.login_ins.ins_sql(self.username, self.user_nw_ip, user_gw_ip, user_gw_cs, self.user_agent, '??????',
                                       '????????????', self.new_date)
                Log.logger.info(log_msg + ' \"fail password_status\"')
                return jsonify({'code': 102})
        else:
            self.login_ins.ins_sql(self.username, self.user_nw_ip, user_gw_ip, user_gw_cs, self.user_agent, '??????',
                                   '???????????????', self.new_date)
            Log.logger.info(log_msg + ' \"fail user_status\"')
            return jsonify({'code': 101})


class UserLogin2(CheckUser):
    def __init__(self):
        super(UserLogin2, self).__init__()
        self.password = request.values.get('password')
        self.user_nw_ip = request.headers.get('X-Real-IP')
        self.user_agent = request.headers.get('User-Agent')
        self.new_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.base = BaseSec()
        self.login_ins = LoginLogSqlalh

        self.ords = ConnRedis(REDIS_CONF['host'], REDIS_CONF['port'])

    def login_dl(self):
        log_msg = 'req_body: [ username=%s, password=%s ] /account/login_dl' % (self.username, self.password)
        user_info = t_acc_user.query.filter_by(name=self.username).first()
        user_gw_ip = request.values.get('user_gw_ip')
        user_gw_cs = request.values.get('user_gw_cs')
        if user_info is not None:
            password_de = self.base.base_de(user_info.password)
            if self.username == user_info.name and self.password == password_de:
                # ??????????????????????????????session
                # session["user"] = self.username
                user_role = t_acc_user.query.filter_by(name=self.username).first()
                user_setting = t_settings.query.filter_by(name='default').first()
                exp_date = user_setting.login_time * 60 * 60
                user_token = hashlib.sha1(os.urandom(24)).hexdigest()
                role_name = self.username + '_role'
                self.ords.conn.set(user_token, self.username)
                self.ords.conn.expire(user_token, exp_date)
                self.ords.conn.set(role_name, user_role.usrole)
                self.ords.conn.set(self.username + '_alias', user_info.alias)
                self.login_ins.ins_sql(self.username, self.user_nw_ip, user_gw_ip, user_gw_cs, self.user_agent, '??????',
                                       None, self.new_date)
                return jsonify({'code': 0, 'token': user_token})
            else:
                self.login_ins.ins_sql(self.username, self.user_nw_ip, user_gw_ip, user_gw_cs, self.user_agent, '??????',
                                       '????????????', self.new_date)
                Log.logger.info(log_msg + ' \"fail password_status\"')
                return jsonify({'code': 102})
        else:
            self.login_ins.ins_sql(self.username, self.user_nw_ip, user_gw_ip, user_gw_cs, self.user_agent, '??????',
                                   '???????????????', self.new_date)
            Log.logger.info(log_msg + ' \"fail user_status\"')
            return jsonify({'code': 101})


class UserRegister(UserLogin):
    def __init__(self):
        super(UserRegister, self).__init__()
        self.email = request.values.get('email')
        self.verification = request.values.get('verification')
        self.ords = ConnRedis(REDIS_CONF['host'], REDIS_CONF['port'])
        self.reg_ins = AccUserSqlalh

    def register(self):
        log_msg = 'req_body: [ username=%s, password=%s, email=%s, verification=%s ] /account/com_register' % (
            self.username, self.password, self.email, self.verification)
        user_chk = t_acc_user.query.filter_by(name=self.username)
        mail_chk = t_acc_user.query.filter_by(mail=self.email)
        if not user_chk is None:
            if not mail_chk is None:
                if not self.ords.conn.get(self.email) is None:
                    if self.verification == self.ords.conn.get(self.email):
                        # self.user_sqlalh.ins_sql(self.username, self.base.base_en(self.password), self.email)
                        self.reg_ins.ins_sql(None, self.username, self.base.base_en(self.password), 'develop',
                                             self.email, None)
                        self.ords.conn.set(self.username + '_alias', 'develop')
                        return jsonify({'code': 0})
                    else:
                        Log.logger.info(log_msg + '\"fail verification\"')
                        return jsonify({'code': 106})
                else:
                    Log.logger.info(log_msg + ' \"fail chk_verification\"')
                    return jsonify({'code': 105})
            else:
                Log.logger.info(log_msg + ' \"fail chk_mail_status\"')
                return jsonify({'code': 104})
        else:
            Log.logger.info(log_msg + ' \"fail chk_user_status\"')
            return jsonify({'code': 103})


class UserAuto:
    def __init__(self):
        self.lt = ListTool()

    @staticmethod
    def user_grp_auto_update(group):
        try:
            host_count = t_acc_user.query.filter_by(group=group).count()
            t_acc_group.query.filter_by(name=group).update({'nums': host_count})
            return True
        except IOError:
            return False


class AccUserDel:
    def __init__(self):
        # self.host_ip = request.values.get('host_ip')
        self.id = request.values.get('id')
        # ????????????????????????
        self.ords = ConnRedis(REDIS_CONF['host'], REDIS_CONF['port'])
        self.user_token = request.cookies.get('ogs_token')
        self.cz_name = self.ords.conn.get(self.user_token)
        self.new_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.ords = ConnRedis(REDIS_CONF['host'], REDIS_CONF['port'])
        self.cz_ins = CzLogSqlalh()
        self.use_auto = UserAuto()

    @property
    def host_del(self):
        log_msg = 'req_body: [ id=%s ] /account/user/del' % self.id
        # user_chk = Host.query.filter_by(host_ip=self.host_ip).first()
        user_chk = t_acc_user.query.filter_by(id=self.id).first()
        if user_chk:
            alias_name = user_chk.name
            db.session.delete(user_chk)
            db.session.commit()
            self.cz_ins.ins_sql(self.cz_name, '????????????', '????????????', self.id, '??????', None, self.new_date)
            self.ords.conn.delete(alias_name + '_alias')
            self.use_auto.user_grp_auto_update(user_chk.group)
            return jsonify({'code': 0})
        else:
            self.cz_ins.ins_sql(self.cz_name, '????????????', '????????????', self.id, '??????', '????????????????????????', self.new_date)
            Log.logger.info(log_msg + ' \"fail acc_user_del_status\"')
            return jsonify({'code': 111})


class AccUserAdd:
    def __init__(self):
        self.alias = request.values.get('alias')
        self.name = request.values.get('name')
        self.password = request.values.get('password')
        self.usrole = request.values.get('usrole')
        self.mail = request.values.get('mail')
        self.group = request.values.get('group')
        self.remarks = request.values.get('remarks', type=str, default=None)
        self.user_ins = AccUserSqlalh()
        self.basesec = BaseSec()
        self.ords = ConnRedis(REDIS_CONF['host'], REDIS_CONF['port'])
        # ????????????????????????
        self.user_token = request.cookies.get('ogs_token')
        self.cz_name = self.ords.conn.get(self.user_token)
        self.new_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.cz_ins = CzLogSqlalh()
        self.use_auto = UserAuto()

    @property
    def host_add(self):
        log_msg = 'req_body: [ alias=%s, name=%s, password=%s, usrole=%s, mail=%s, group=%s, remarks=%s ] ' \
                  '/account/user/add' % (
                      self.alias, self.name, self.password, self.usrole, self.mail, self.group,
                      self.remarks)
        try:
            user_chk = t_acc_user.query.filter_by(name=self.name).first()
            if user_chk is None:
                password_en = self.basesec.base_en(self.password)
                self.user_ins.ins_sql(self.alias, self.name, password_en, self.usrole, self.mail, self.group,
                                      self.remarks)
                self.cz_ins.ins_sql(self.cz_name, '????????????', '????????????', self.name, '??????', None, self.new_date)
                self.ords.conn.set(self.name + '_alias', self.alias)
                self.use_auto.user_grp_auto_update(self.group)
                return jsonify({'code': 0})
            else:
                self.cz_ins.ins_sql(self.cz_name, '????????????', '????????????', self.name, '??????', '??????????????????', self.new_date)
                Log.logger.info(log_msg + ' \"fail sel_fail\"')
                return jsonify({'code': 111})
        except IOError:
            self.cz_ins.ins_sql(self.cz_name, '????????????', '????????????', self.name, '??????', '?????????????????????', self.new_date)
            Log.logger.info(log_msg + ' \"fail con_fail\"')
            return jsonify({'code': 201})
        except Exception:
            self.cz_ins.ins_sql(self.cz_name, '????????????', '????????????', self.name, '??????', '????????????', self.new_date)
            Log.logger.info(log_msg + ' \"fail\"')
            return jsonify({'code': 2})


class AccUserUpdate(AccUserAdd):
    def __init__(self):
        super(AccUserUpdate, self).__init__()
        self.id = request.values.get('id')

    @property
    def update(self):
        log_msg = 'req_body: [ id=%s, alias=%s, name=%s, password=%s, usrole=%s, mail=%s, remarks=%s ] ' \
                  '/account/user/update' % (
                      self.id, self.alias, self.name, self.password, self.usrole, self.mail, self.remarks)
        try:
            password_en = self.basesec.base_en(self.password)
            up_user = t_acc_user.query.filter_by(id=self.id).first()
            t_acc_user.query.filter_by(id=self.id).update({'alias': self.alias, 'name': self.name,
                                                           'password': password_en,
                                                           'usrole': self.usrole,
                                                           'group': self.group,
                                                           'mail': self.mail, 'remarks': self.remarks})
            db.session.commit()
            role_name = self.name + '_role'
            self.ords.conn.set(role_name, self.usrole)
            self.cz_ins.ins_sql(self.cz_name, '????????????', '????????????', self.name, '??????', None, self.new_date)
            self.ords.conn.set(self.name + '_alias', self.alias)
            if up_user.group == self.group:
                self.use_auto.user_grp_auto_update(self.group)
            else:
                self.use_auto.user_grp_auto_update(up_user.group)
                self.use_auto.user_grp_auto_update(self.group)
            return jsonify({'code': 0})
        except Exception:
            self.cz_ins.ins_sql(self.cz_name, '????????????', '????????????', self.name, '??????', '?????????????????????', self.new_date)
            Log.logger.info(log_msg + ' \"fail\"')
            return jsonify({'code': 2})


class UserLogout:
    def __init__(self):
        self.ords = ConnRedis(REDIS_CONF['host'], REDIS_CONF['port'])
        self.user_token = request.cookies.get('ogs_token')

    def logout(self):
        if self.ords.conn.get(str(self.user_token)) is None:
            return {'code': 3, 'msg': '???????????????'}
        else:
            self.ords.conn.delete(self.user_token)
            return {'code': 0}