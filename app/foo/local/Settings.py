from flask import request, jsonify
from app.sqldb.SqlAlchemyDB import t_settings, db
from app.sqldb.SqlAlchemyInsert import SettingsSqlalh
from app.tools.SqlListTool import ListTool
from app.tools.redisdb import ConnRedis, REDIS_CONF
from app.tools.at import Log


class OgsSettings:
    def __init__(self):
        self.ords = ConnRedis(REDIS_CONF['host'], REDIS_CONF['port'])
        self.user_token = request.cookies.get('ogs_token')
        self.name = self.ords.conn.get(self.user_token)
        self.lt = ListTool()
        self.set_ins = SettingsSqlalh()

    @staticmethod
    def settings_open_info():
        default_msg = t_settings.query.filter_by(name='default').first()
        return {'name': default_msg.name, 'login_time': default_msg.login_time,
                'register_status': default_msg.register_status}

    def settings_info(self):
        default_msg = t_settings.query.filter_by(name='default').first()
        st_msg = self.lt.dict_reset_pop_auto(default_msg)
        return jsonify(st_msg)

    def settings_change(self):
        log_msg = 'req_body: [ name=%s ] /local/settings/update (fail)' % self.name
        try:
            login_time = request.values.get('login_time')
            register_status = request.values.get('register_status')
            color_matching = request.values.get('color_matching')
            # query_msg = t_settings.query.filter_by(name=self.name).first()
            # if query_msg is None:
            #     self.set_ins.ins_sql(self.name, login_time, register_status, color_matching)
            #     return jsonify({'code': 0})
            # else:
            if self.ords.conn.get(self.name + '_role') == 'admin':
                t_settings.query.filter_by(name='default').update(
                    {'login_time': login_time, 'register_status': register_status,
                     'color_matching': color_matching})
                db.session.commit()
                return jsonify({'code': 0})
            else:
                return jsonify({'code': 4})
        except IOError:
            Log.logger.info(log_msg + ' \"fail"')
            return jsonify({'code': 201})
