import sys
from flask import request, jsonify
from app.tools.redisdb import ConnRedis
from app.sqldb.SqlAlchemyDB import t_host, t_group, t_line_chart, t_acc_user, t_login_log, t_acc_group, t_command_log, \
    t_auth_host, t_sys_user
from app.conf.conf_test import REDIS_CONF


class AppInit:
    def __init__(self):
        self.res = ConnRedis(REDIS_CONF['host'], REDIS_CONF['port'])
        self.mysql_list = [t_host, t_group, t_line_chart, t_acc_user, t_login_log, t_acc_group, t_command_log,
                           t_auth_host, t_sys_user]

    def con_init(self):
        if self.res.status_red() is False:
            print('error! redis is not connection')
            sys.exit(1)
        for i in self.mysql_list:
            try:
                i.query.count()
            except IOError:
                print('error! mysql database table {} is not found'.format(str(i)))
                sys.exit(2)

    @staticmethod
    def app_status():
        sta = request.values.get('status')
        if sta == 'ogsfront':
            return jsonify({'status': 200})
        else:
            return jsonify({'status': 403})
