import datetime, os
from PIL import Image
from flask import request, jsonify, make_response
from app.sqldb.SqlAlchemyDB import t_host, db, t_group, t_sys_user, t_acc_user, t_auth_host, t_login_log, t_line_chart
from app.tools.SqlListTool import ListTool
from app.sqldb.SqlAlchemyInsert import LineChartSqlalh
from app.conf.conf_test import FILE_CONF
from app.tools.at import auth_list_get


class CountUpdate:
    def __init__(self):
        self.ls_tool = ListTool()
        self.line_ins = LineChartSqlalh
        self.now_date = datetime.date.today()
        self.query_user_count = t_login_log.query.filter(
            t_login_log.login_time.like("%{}%".format(self.now_date))).filter_by(login_status='成功').with_entities(
            t_login_log.login_name).distinct().count()
        self.query_login_count = t_login_log.query.filter(
            t_login_log.login_time.like("%{}%".format(self.now_date))).count()
        self.query_msg = t_line_chart.query.filter_by(chart_date=self.now_date).first()

    @property
    def count_into_all(self):
        try:
            if self.query_msg is None:
                self.line_ins.ins_sql(self.query_login_count, self.query_user_count, self.now_date)
            return jsonify({'code': 0})
        except IOError:
            return jsonify({'code': 201})

    @property
    def count_update_all(self):
        try:
            if self.query_msg is None:
                self.count_into_all()
            elif self.query_msg is not None:
                t_line_chart.query.filter_by(chart_date=self.now_date).update(
                    {'login_count': self.query_login_count, 'user_count': self.query_user_count,
                     'chart_date': self.now_date})
                db.session.commit()
            return jsonify({'code': 0})
        except IOError:
            return jsonify({'code': 201})


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
            return jsonify({'code': 201})

    @property
    def server_chart_count_all(self):
        try:
            login_list = []
            user_list = []
            date_list = []
            new_date = (datetime.date.today() - datetime.timedelta(days=-5)).strftime("%Y-%m-%d")
            old_date = (datetime.date.today() - datetime.timedelta(days=+15)).strftime("%Y-%m-%d")
            now_date = datetime.date.today()
            query_msg_all = t_line_chart.query.filter(t_line_chart.chart_date <= now_date).filter(
                t_line_chart.chart_date >= old_date).all()
            for i in query_msg_all:
                query_msg = i.__dict__
                date_list.append(str(query_msg['chart_date']))
                login_list.append(query_msg['login_count'])
                user_list.append(query_msg['user_count'])
                # login_list.append({'date': str(query_msg['chart_date']), 'value': query_msg['login_count']})
                # user_list.append({'date': str(query_msg['chart_date']), 'value': query_msg['user_count']})
            # return jsonify({'code': 0, 'login_msg': login_list, 'user_msg': user_list})
            return jsonify({'code': 0, 'date_msg': date_list, 'login_msg': login_list, 'user_msg': user_list})
        except IOError:
            jsonify({'code': 201})


class DataList:
    def __init__(self):
        self.lt = ListTool()

    def get_list(self):
        # que_group = Host.query.with_entities(Host.group).all()
        que_group = t_group.query.with_entities(t_group.name).all()
        host_group = self.lt.list_rep_gather(que_group)
        res_group = auth_list_get()
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
        return jsonify({"code": 0, "host": [{'title': '所有资产组', 'id': 0, 'spread': 'true', 'children': msg_list}]})


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


class GetUserImage:
    def __init__(self):
        # self.path = '/data/putfile/'
        self.path = FILE_CONF['image_path']
        self.default_img = 'juzi11.png'

    def get_img(self, img_name):
        request_begin_time = datetime.date.today()
        try:
            # 根据图片名显示对应路径图片
            if os.path.isfile(self.path + img_name + '.png'):
                image_data = open(self.path + img_name + '.png', "rb").read()
            else:
                image_data = open(self.path + self.default_img, "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response
        except FileNotFoundError:
            return jsonify({'image': 'error not file'})


class PutUserImage:
    def __init__(self):
        # self.path = '/data/putfile/'
        self.path = FILE_CONF['image_path']
        self.img_file = request.files.get('file')
        self.img_user = request.values.get('user')

    def put_img(self):
        im = Image.open(self.img_file)
        im.save(self.path + self.img_user + '.png')
        return jsonify({'status': 'true'})
