import time, datetime
from flask import request, jsonify
from app.sqldb.SqlAlchemyDB import t_host, db, t_group, t_sys_user, t_acc_user, t_auth_host, t_login_log, t_line_chart
from app.tools.SqlListTool import ListTool
from app.sqldb.SqlAlchemyInsert import LineChartSqlalh


class Count_update:
    def __init__(self):
        self.ls_tool = ListTool()
        self.line_ins = LineChartSqlalh
        self.now_date = time.strftime("%Y-%m-%d", time.localtime())

    @property
    def count_update_all(self):
        try:
            query_user_count = t_login_log.query.filter(
                t_login_log.login_time.like("%{}%".format(self.now_date))).filter_by(login_status='成功').with_entities(
                t_login_log.login_name).distinct().count()
            query_login_count = t_login_log.query.filter(
                t_login_log.login_time.like("%{}%".format(self.now_date))).count()
            self.line_ins.ins_sql(self.now_date, query_login_count, query_user_count)
            print(query_user_count, query_login_count)
            return jsonify({'status': 'true'})
        except IOError:
            return jsonify({'status': 'fail'})


class CountList:
    def __init__(self):
        self.lt = ListTool()

    @property
    def server_count_all(self):
        try:
            host_len_msg = t_host.query.count()
            user_len_msg = t_acc_user.query.count()
            group_len_msg = t_group.query.count()
            return jsonify({
                'code': 0,
                'host_len': host_len_msg,
                'user_len': user_len_msg,
                'group_len': group_len_msg,
                'container_len': 0
            })
        except IOError:
            return jsonify({'code': 1})

    @property
    def server_chart_count_all(self):
        try:
            login_list = []
            user_list = []
            new_date = (datetime.date.today() - datetime.timedelta(days=-5)).strftime("%Y-%m-%d")
            old_date = (datetime.date.today() - datetime.timedelta(days=+5)).strftime("%Y-%m-%d")
            query_msg_all = t_line_chart.query.filter(t_line_chart.chart_date <= new_date).filter(
                t_line_chart.chart_date >= old_date).all()
            for i in query_msg_all:
                query_msg = i.__dict__
                login_list.append({'date': query_msg['chart_date'], 'value': query_msg['login_count']})
                user_list.append({'date': query_msg['chart_date'], 'value': query_msg['user_count']})
            return jsonify({'login_msg': login_list, 'user_msg': user_list})
        except IOError:
            jsonify({'status': 'fail'})


class DataList:
    def __init__(self):
        self.lt = ListTool()

    def get_list(self):
        # que_group = Host.query.with_entities(Host.group).all()
        que_group = t_group.query.with_entities(t_group.name).all()
        host_group = self.lt.list_rep_gather(que_group)
        name = request.values.get('name')
        que_auth_group = t_auth_host.query.filter(t_auth_host.user.like("%{}%".format(name))).all()
        res_group = set(self.lt.auth_ls_list_que(que_auth_group))
        print(res_group)
        group_count = 1000
        # host_count = 100
        msg_list = []
        for i in res_group:
            body_list = []
            group_count += 1
            dic = t_host.query.filter_by(group=i).all()
            for y in dic:
                # host_count += 1
                host_id = y.id
                host_name = y.alias
                body_list.append({'title': host_name, 'id': host_id})
            dic = {'title': i, 'id': group_count, 'children': body_list}
            msg_list.append(dic)
        return jsonify({"host": [{'title': '所有资产组', 'id': 0, 'spread': 'true', 'children': msg_list}]})


class DataSumAll:
    def __init__(self):
        self.lt = ListTool()
        self.sum_name = request.values.get('sum_name')

    def get_sum(self):
        if self.sum_name == 'group':
            try:
                query_group = t_group.query.with_entities(t_group.name).all()
                group_list = self.lt.list_rep_gather(query_group)
                for i in group_list:
                    group_count = t_host.query.filter_by(group=i).count()
                    t_group.query.filter_by(name=i).update({'nums': group_count})
                    db.session.commit()
                    return jsonify({'update_table_sum': 'true'})
            except IOError:
                return jsonify({'update_table_sum': 'fail'})

        elif self.sum_name == 'sys_user':
            try:
                query_sys_user = t_sys_user.query.with_entities(t_sys_user.host_user).all()
                sys_user_list = self.lt.list_rep_gather(query_sys_user)
                for i in sys_user_list:
                    sys_user_count = t_host.query.filter_by(host_user=i).count()
                    t_sys_user.query.filter_by(host_user=i).update({'host_user': sys_user_count})
                    db.session.commit()
                    return jsonify({'update_table_sum': 'true'})
            except IOError:
                return jsonify({'update_table_sum': 'fail'})
