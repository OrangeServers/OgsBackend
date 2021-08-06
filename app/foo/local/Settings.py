from flask import request, jsonify
from app.sqldb.SqlAlchemyDB import t_settings, db
from app.sqldb.SqlAlchemyInsert import SettingsSqlalh
from app.tools.SqlListTool import ListTool
from app.tools.at import Log


class OgsSettings:
    def __init__(self):
        self.name = request.values.get('name')
        self.lt = ListTool()
        self.set_ins = SettingsSqlalh()

    def settings_info(self):
        query_msg = t_settings.query.filter_by(name=self.name).first()
        if query_msg is None:
            default_msg = t_settings.query.filter_by(name='default').first()
            st_msg = self.lt.dict_reset_pop_auto(default_msg)
            Log.logger.info('req_body: [ %s=%s ] /local/settings/get (true)' % ('name', self.name))
            return jsonify(st_msg)
        else:
            st_msg = self.lt.dict_reset_pop_auto(query_msg)
            Log.logger.info('req_body: [ %s=%s ] /local/settings/get (default true)' % ('name', self.name))
            return jsonify(st_msg)

    def settings_change(self):
        try:
            login_time = request.values.get('login_time')
            register_status = request.values.get('register_status')
            color_matching = request.values.get('color_matching')
            query_msg = t_settings.query.filter_by(name=self.name).first()
            if query_msg is None:
                self.set_ins.ins_sql(self.name, login_time, register_status, color_matching)
                Log.logger.info('req_body: [ %s=%s, %s=%s, %s=%s, %s=%s ] /local/settings/update (insert true)' % (
                    'name', self.name, 'login_time', login_time, 'register_status', register_status, 'color_matching',
                    color_matching))
                return jsonify({'status': 'true'})
            else:
                t_settings.query.filter_by(name=self.name).update(
                    {'name': self.name, 'login_time': login_time, 'register_status': register_status,
                     'color_matching': color_matching})
                db.session.commit()
                Log.logger.info('req_body: [ %s=%s, %s=%s, %s=%s, %s=%s ] /local/settings/update (update true)' % (
                    'name', self.name, 'login_time', login_time, 'register_status', register_status, 'color_matching',
                    color_matching))
                return jsonify({'status': 'true'})
        except IOError:
            Log.logger.info('req_body: [ %s=%s ] /local/settings/update (fail)' % (
                'name', self.name))
            return jsonify({'status': 'fail'})
