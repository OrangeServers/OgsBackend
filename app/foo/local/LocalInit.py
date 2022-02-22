import sys, os
from flask import request, jsonify
from app.tools.redisdb import ConnRedis
from app.sqldb.SqlAlchemyDB import t_host, t_group, t_line_chart, t_acc_user, t_login_log, t_acc_group, t_command_log, \
    t_auth_host, t_sys_user
from app.conf.conf_test import REDIS_CONF, DEFAULT_DATA_DIR, FILE_CONF
from app.tools.at import Log


class AppInit:
    def __init__(self):
        self.ords = ConnRedis(REDIS_CONF['host'], REDIS_CONF['port'])
        self.mysql_list = [t_host, t_group, t_line_chart, t_acc_user, t_login_log, t_acc_group, t_command_log,
                           t_auth_host, t_sys_user]
        self.Log = Log

    def con_init(self):
        self.Log.logger.info('check connection redis............')
        self.Log.logger.info('check connection mysql............')
        if self.ords.conn.ping() is False:
            self.Log.logger.error('error! redis is not connection')
            sys.exit(1)
        for i in self.mysql_list:
            try:
                i.query.count()
            except IOError:
                self.Log.logger.error('error! mysql database table {} is not found'.format(str(i)))
                sys.exit(2)
        self.Log.logger.info('check connection redis mysql is ok!')
        if os.path.exists(DEFAULT_DATA_DIR):
            if not os.path.exists(FILE_CONF['image_path']):
                os.mkdir(FILE_CONF['image_path'])
                self.Log.logger.info('mkdir is image_path')
            if not os.path.exists(FILE_CONF['file_path']):
                os.mkdir(FILE_CONF['file_path'])
                self.Log.logger.info('mkdir is file_path')
            if not os.path.exists(FILE_CONF['key_path']):
                os.mkdir(FILE_CONF['key_path'])
                self.Log.logger.info('mkdir is key_path')
        else:
            os.mkdir(DEFAULT_DATA_DIR)
            os.mkdir(FILE_CONF['image_path'])
            os.mkdir(FILE_CONF['file_path'])
            os.mkdir(FILE_CONF['key_path'])
            self.Log.logger.info('mkdir is data and subdirectory......')

    def app_status(self):
        sta = request.values.get('status')
        log_msg = 'req_body: [ status=%s ] /local/init' % sta
        if sta == 'ogsfront':
            return jsonify({'status': 200})
        else:
            self.Log.logger.error(log_msg + ' \"fail 403\"')
            return jsonify({'status': 403})

    @staticmethod
    def app_auth_status():
        return {'code': 0}
