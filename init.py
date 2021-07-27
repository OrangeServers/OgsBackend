# -*- coding=utf8 -*-
import argparse
from Flask_App_Settings import *
from geventwebsocket.handler import WebSocketHandler  # 提供WS（websocket）协议处理
from geventwebsocket.server import WSGIServer  # websocket服务承载
from datetime import timedelta
from app.service.local_api import *
from app.service.user_login_api import *
from app.service.acc_group import *
from app.service.logs_api import *
from app.service.mail_api import *
from app.service.server_group_api import *
from app.service.server_mag_api import *
from app.service.ser_acc_user_api import *
from app.service.server_sysuser_api import *
from app.service.auth_api import *

# 导入skywalking链路追踪
import asyncio
from skywalking import agent, config

config.init(collector='10.0.1.198:11800', service='orangeserver')  # 采集服务的地址，给自己的服务起个名称
agent.start()

# 导入elastic apm链路追踪
from elasticapm.contrib.flask import ElasticAPM

app.config['ELASTIC_APM'] = {
    # Set required service name. Allowed characters:
    # a-z, A-Z, 0-9, -, _, and space
    'SERVICE_NAME': 'orangeserver',

    # Use if APM Server requires a token
    'SECRET_TOKEN': '',

    # Set custom APM Server URL (default: http://localhost:8200)
    'SERVER_URL': 'http://10.0.1.198:8200',
}

apm = ElasticAPM(app)
# 原有导入模块 --------------------------------------------------------------------------------------
# from flask import render_template, make_response
# from app.foo.user.decorator import wrapper

# 异步导入相关模块 ------------------------------------------------------------------------------------
# from gevent import monkey
# from gevent.pywsgi import WSGIServer
# from geventwebsocket.handler import WebSocketHandler

# monkey.patch_all()
# 初始化flask实例
# app = Flask(__name__, static_folder='./static', template_folder='')
app.config.update(DEBUG=False)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
app.logger.info('info log')
app.logger.warning('warning log')
app.logger.error('error log')

# 赋予session值的密钥,前后端分离后已经不用
app.secret_key = "!@#$%^&*()"


# 执行脚本时指定启动参数的函数
def sta_cs():
    parser = argparse.ArgumentParser('请输入 --host  --port 参数')
    parser.add_argument("--host", help="listen host", default='0.0.0.0')
    parser.add_argument("--port", help="port", default=28000)
    # parser.add_argument("--port", help="port", required=True)
    args = parser.parse_args()
    return args


"""  各接口详解：
        /server/    操作资产主机接口
        /mail/    发送邮件相关接口
        /local/    本地执行命令接口
"""


@app.route('/')
# @wrapper
def index():
    return 'hello from OrangeServer api server', 200


def orange_init_api():
    # 服务状态
    app.add_url_rule('/local/init', view_func=local_app_status, methods=['POST', 'get'])

    # 发送邮件
    app.add_url_rule('/mail/send_user_mail', view_func=mail_send_user, methods=['POST', 'get'])
    app.add_url_rule('/mail/send_mail', view_func=mail_send, methods=['POST', 'get'])

    # 用户注册登录
    app.add_url_rule('/account/login_dl', view_func=acc_login_dl, methods=['POST', 'get'])
    app.add_url_rule('/account/chk_username', view_func=acc_chk_username, methods=['POST', 'get'])
    app.add_url_rule('/account/com_register', view_func=acc_com_register, methods=['POST', 'get'])

    # 用户登录日志
    app.add_url_rule('/account/login/logs', view_func=acc_login_logs, methods=['POST', 'get'])
    app.add_url_rule('/account/login/date', view_func=acc_login_date, methods=['POST', 'get'])
    app.add_url_rule('/account/login/select', view_func=acc_login_select, methods=['POST', 'get'])

    # 用户执行命令日志
    app.add_url_rule('/server/command/logs', view_func=server_com_logs, methods=['POST', 'get'])
    app.add_url_rule('/server/command/date', view_func=server_com_date, methods=['POST', 'get'])
    app.add_url_rule('/server/command/select', view_func=server_com_select, methods=['POST', 'get'])

    # 用户操作日志
    app.add_url_rule('/server/cz/logs', view_func=server_cz_logs, methods=['POST', 'get'])
    app.add_url_rule('/server/cz/date', view_func=server_cz_date, methods=['POST', 'get'])
    app.add_url_rule('/server/cz/select', view_func=server_cz_select, methods=['POST', 'get'])

    # 用户组接口
    app.add_url_rule('/account/group/list', view_func=acc_group_list, methods=['POST', 'get'])
    app.add_url_rule('/account/group/list_all', view_func=acc_group_list_all, methods=['POST', 'get'])
    app.add_url_rule('/account/group/add', view_func=acc_group_add, methods=['POST', 'get'])
    app.add_url_rule('/account/group/update', view_func=acc_group_update, methods=['POST', 'get'])
    app.add_url_rule('/account/group/del', view_func=acc_group_del, methods=['POST', 'get'])

    # 这里是页面用户接口
    app.add_url_rule('/account/user/list', view_func=acc_user_list, methods=['POST', 'get'])
    app.add_url_rule('/account/user/auth_list', view_func=acc_user_auth_list, methods=['POST', 'get'])
    app.add_url_rule('/account/user/list_all', view_func=acc_user_list_all, methods=['POST', 'get'])
    app.add_url_rule('/account/user/add', view_func=acc_user_add, methods=['POST', 'get'])
    app.add_url_rule('/account/user/update', view_func=acc_user_update, methods=['POST', 'get'])
    app.add_url_rule('/account/user/del', view_func=acc_user_del, methods=['POST', 'get'])

    # 这里是系统用户接口
    app.add_url_rule('/server/sys/user/list', view_func=sys_user_list, methods=['POST', 'get'])
    app.add_url_rule('/server/sys/user/list_all', view_func=sys_user_list_all, methods=['POST', 'get'])
    app.add_url_rule('/server/sys/user/add', view_func=sys_user_add, methods=['POST', 'get'])
    app.add_url_rule('/server/sys/user/update', view_func=sys_user_update, methods=['POST', 'get'])
    app.add_url_rule('/server/sys/user/del', view_func=sys_user_del, methods=['POST', 'get'])

    # 这里是资产主机接口
    app.add_url_rule('/server/host/add', view_func=server_add, methods=['POST', 'get'])
    app.add_url_rule('/server/host/update', view_func=server_update, methods=['POST', 'get'])
    app.add_url_rule('/server/host/del', view_func=server_del, methods=['POST', 'get'])
    app.add_url_rule('/server/host/cmd', view_func=server_cmd, methods=['POST', 'get'])
    app.add_url_rule('/server/host/list_all', view_func=host_list_all, methods=['POST', 'get'])
    app.add_url_rule('/server/host/list', view_func=host_list, methods=['POST', 'get'])
    app.add_url_rule('/server/host/list_page', view_func=host_list_page, methods=['POST', 'get'])
    app.add_url_rule('/server/group_list', view_func=group_list, methods=['POST', 'get'])
    app.add_url_rule('/server/group/cmd', view_func=group_cmd, methods=['POST', 'get'])
    app.add_url_rule('/server/host_list_cmd', view_func=server_list_cmd, methods=['POST', 'get'])
    app.add_url_rule('/server/file/put', view_func=server_file, methods=['POST', 'get'])

    # 这里是资产组接口
    app.add_url_rule('/server/host/group/list', view_func=host_group_list, methods=['POST', 'get'])
    app.add_url_rule('/server/host/group/list_all', view_func=host_group_list_all, methods=['POST', 'get'])
    app.add_url_rule('/server/host/group/name_list', view_func=host_group_name_list, methods=['POST', 'get'])
    app.add_url_rule('/server/host/group/add', view_func=host_group_add, methods=['POST', 'get'])
    app.add_url_rule('/server/host/group/update', view_func=host_group_update, methods=['POST', 'get'])
    app.add_url_rule('/server/host/group/del', view_func=host_group_del, methods=['POST', 'get'])

    # 这里是权限管理接口
    app.add_url_rule('/auth/host/list_all', view_func=auth_host_list_all, methods=['POST', 'get'])
    app.add_url_rule('/auth/host/add', view_func=auth_host_add, methods=['POST', 'get'])
    app.add_url_rule('/auth/host/del', view_func=auth_host_del, methods=['POST', 'get'])
    app.add_url_rule('/auth/host/update', view_func=auth_host_update, methods=['POST', 'get'])
    app.add_url_rule('/auth/host/uplist', view_func=auth_group_uplist, methods=['POST', 'get'])
    app.add_url_rule('/auth/host/list', view_func=auth_create_get_list, methods=['POST', 'get'])

    # 这里是本地执行接口
    app.add_url_rule('/local/dir/group', view_func=local_dir_group, methods=['POST', 'get'])
    app.add_url_rule('/local/dir/project', view_func=local_dir_project, methods=['POST', 'get'])
    app.add_url_rule('/local/rsync', view_func=local_rsync_code, methods=['POST', 'get'])
    app.add_url_rule('/local/sum', view_func=local_data_sum, methods=['POST', 'get'])
    app.add_url_rule('/local/data', view_func=local_data_list, methods=['POST', 'get'])
    app.add_url_rule('/local/file', view_func=local_data_file_put, methods=['POST', 'get'])

    # 这里是主页图标数据接口
    app.add_url_rule('/server/count_list_all', view_func=count_list, methods=['POST', 'get'])
    app.add_url_rule('/local/chart/count', view_func=local_chart_count_all, methods=['POST', 'get'])
    app.add_url_rule('/local/chart/update', view_func=local_chart_update, methods=['POST', 'get'])
    app.add_url_rule('/local/image/test_get/<img_name>', view_func=local_image_get, methods=['POST', 'get'])
    app.add_url_rule('/local/image/test_put', view_func=local_image_put, methods=['POST', 'get'])
    app.add_url_rule('/local/settings/get', view_func=local_settings_get, methods=['POST', 'get'])
    app.add_url_rule('/local/settings/update', view_func=local_settings_update, methods=['POST', 'get'])

    # 文件类型操作
    app.add_url_rule('/local/download', view_func=file_download, methods=['POST', 'get'])
    app.add_url_rule('/local/file/def_get', view_func=file_def_get, methods=['POST', 'get'])
    app.add_url_rule('/local/file/add', view_func=file_create, methods=['POST', 'get'])
    app.add_url_rule('/local/file/del', view_func=file_remove, methods=['POST', 'get'])
    app.add_url_rule('/local/file/put', view_func=file_save, methods=['POST', 'get'])

    # ssh专用websocket接口
    app.add_url_rule('/local/websocket', view_func=local_web_ssh)
    with app.app_context():
        local_app_init()
        local_chart_into()


if __name__ == "__main__":
    orange_init_api()
    # app.run(host='0.0.0.0',port=28000)
    http_server = WSGIServer(('0.0.0.0', 28000), application=app, handler_class=WebSocketHandler)
    http_server.serve_forever()
    # args = sta_cs()
    # host = args.host
    # port = args.port
    # app.run(host=host, port=port)
    # http_server = WSGIServer((host,port),app,handler_class=WebSocketHandler)
    # http_server.serve_forever()
    # 使用 asyncio, 也可以不用，不影响链路追踪
    # AsyncIOMainLoop().install()
    # app_server = Application().listen(options.port)
    # try:
    #     asyncio.get_event_loop().run_forever()
    # except KeyboardInterrupt:
    #     print()
    #     print("stopping...")
    #     print()
