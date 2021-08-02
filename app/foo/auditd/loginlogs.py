from flask import request, jsonify
from app.sqldb.SqlAlchemyDB import t_login_log, t_command_log, t_cz_log
from app.tools.SqlListTool import ListTool


class LoginLogs:
    def __init__(self):
        self.lt = ListTool()
        self.table_page = request.values.get('page')
        self.table_limit = request.values.get('limit')
        self.table_offset = (int(self.table_page) - 1) * 10

    def get_login_logs(self):
        try:
            # query_msg = t_login_log.query.offset(self.table_offset).limit(self.table_limit).all()
            query_msg = t_login_log.query.order_by(t_login_log.login_time.desc()).offset(self.table_offset).limit(self.table_limit).all()
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
            query_msg = t_login_log.query.filter(t_login_log.login_name.like("%{}%".format(login_jg_date))).offset(
                self.table_offset).limit(self.table_limit).all()
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


class CommandLogs:
    def __init__(self):
        self.lt = ListTool()
        self.table_page = request.values.get('page')
        self.table_limit = request.values.get('limit')
        self.table_offset = (int(self.table_page) - 1) * 10

    def get_com_logs(self):
        try:
            query_msg = t_command_log.query.order_by(t_command_log.com_time.desc()).offset(self.table_offset).limit(self.table_limit).all()
            list_msg = self.lt.time_ls_dict_que(query_msg, 'id', 'com_time')
            len_msg = t_command_log.query.count()
            return jsonify({"host_status": 0,
                            "command_list_msg": list_msg,
                            "msg": "",
                            "command_len_msg": len_msg})
        except IOError:
            return jsonify({"command_list_msg": 'select list msg error',
                            "command_len_msg": 0})

    def get_select_logs(self):
        com_jg_date = request.values.get('com_jg_date')
        try:
            query_msg = t_command_log.query.filter(t_command_log.com_name.like("%{}%".format(com_jg_date))).offset(
                self.table_offset).limit(self.table_limit).all()
            list_msg = self.lt.time_ls_dict_que(query_msg, 'id', 'com_time')
            len_msg = t_command_log.query.filter(t_command_log.com_name.like("%{}%".format(com_jg_date))).count()
            return jsonify({"host_status": 0,
                            "command_list_msg": list_msg,
                            "msg": "",
                            "command_len_msg": len_msg})
        except IOError:
            return jsonify({"command_list_msg": 'select list msg error',
                            "command_len_msg": 0})

    def get_date_logs(self):
        com_jg_date = request.values.get('com_jg_date')
        type(com_jg_date)
        msg = com_jg_date.split(' - ')
        try:
            query_msg = t_command_log.query.filter(t_command_log.com_time >= msg[0]).filter(
                t_command_log.com_time <= msg[1]).order_by(t_command_log.com_time.desc()).offset(
                self.table_offset).limit(self.table_limit).all()
            list_msg = self.lt.time_ls_dict_que(query_msg, 'id', 'com_time')
            len_msg = t_command_log.query.filter(t_command_log.com_time >= msg[0]).filter(
                t_command_log.com_time <= msg[1]).order_by(t_command_log.com_time.desc()).count()
            return jsonify({"host_status": 0,
                            "command_list_msg": list_msg,
                            "msg": "",
                            "command_len_msg": len_msg})
        except IOError:
            return jsonify({"command_list_msg": 'select list msg error',
                            "command_len_msg": 0})


class CzLogs:
    def __init__(self):
        self.lt = ListTool()
        self.table_page = request.values.get('page')
        self.table_limit = request.values.get('limit')
        self.table_offset = (int(self.table_page) - 1) * 10

    def get_cz_logs(self):
        try:
            query_msg = t_cz_log.query.order_by(t_cz_log.cz_time.desc()).offset(self.table_offset).limit(self.table_limit).all()
            list_msg = self.lt.time_ls_dict_que(query_msg, 'id', 'cz_time')
            len_msg = t_cz_log.query.count()
            return jsonify({"host_status": 0,
                            "cz_list_msg": list_msg,
                            "msg": "",
                            "cz_len_msg": len_msg})
        except IOError:
            return jsonify({"cz_list_msg": 'select list msg error',
                            "cz_len_msg": 0})

    def get_select_logs(self):
        cz_jg_date = request.values.get('cz_jg_date')
        try:
            query_msg = t_cz_log.query.filter(t_cz_log.cz_name.like("%{}%".format(cz_jg_date))).offset(
                self.table_offset).limit(self.table_limit).all()
            list_msg = self.lt.time_ls_dict_que(query_msg, 'id', 'com_time')
            len_msg = t_cz_log.query.filter(t_cz_log.cz_name.like("%{}%".format(cz_jg_date))).count()
            return jsonify({"host_status": 0,
                            "cz_list_msg": list_msg,
                            "msg": "",
                            "cz_len_msg": len_msg})
        except IOError:
            return jsonify({"cz_list_msg": 'select list msg error',
                            "cz_len_msg": 0})

    def get_date_logs(self):
        cz_jg_date = request.values.get('cz_jg_date')
        type(cz_jg_date)
        msg = cz_jg_date.split(' - ')
        try:
            query_msg = t_cz_log.query.filter(t_cz_log.cz_time >= msg[0]).filter(
                t_cz_log.cz_time <= msg[1]).order_by(t_cz_log.cz_time.desc()).offset(
                self.table_offset).limit(self.table_limit).all()
            list_msg = self.lt.time_ls_dict_que(query_msg, 'id', 'com_time')
            len_msg = t_cz_log.query.filter(t_cz_log.cz_time >= msg[0]).filter(
                t_cz_log.cz_time <= msg[1]).order_by(t_cz_log.cz_time.desc()).count()
            return jsonify({"host_status": 0,
                            "cz_list_msg": list_msg,
                            "msg": "",
                            "cz_len_msg": len_msg})
        except IOError:
            return jsonify({"cz_list_msg": 'select list msg error',
                            "cz_len_msg": 0})
