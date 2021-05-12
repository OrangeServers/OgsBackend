# -*- coding=utf8 -*-
from flask import jsonify
from Flask_App_Settings import *
from datetime import timedelta
import argparse
from app.foo.local.Basics import CountList, DataList, DataSumAll
from app.foo.property.ServerManagement import ServerAdd, ServerList, ServerCmd2, ServerListCmd, ServerDel, GroupCmd, GroupList, ServerUpdate, ServerScript
from app.foo.user.AccUser import UserLogin, CheckUser, CheckMail, UserRegister, LoginLogs
from app.foo.user.user import AccUserList, AccUserAdd, AccUserUpdate, AccUserDel
from app.foo.property.SysUser import SysUserList, SysUserAdd, SysUserUpdate, SysUserDel
from app.foo.property.ServerGroup import AccGroupList, AccGroupAdd, AccGroupUpdate, AccGroupDel
from app.conf.conf_test import *
from app.foo.local.LocalShell import LocalDirList
from app.foo.mail.MailApi import OrangeMailApi


# 原有导入模块 --------------------------------------------------------------------------------------
# from flask import render_template, make_response
# from app.foo.user.decorator import wrapper
# from app.tools.SqlListTool import ListTool
# from app.sqldb.SqlAlchemyDB import User2, Host

# 异步导入相关模块 ------------------------------------------------------------------------------------
# from gevent import monkey
# from gevent.pywsgi import WSGIServer
# from geventwebsocket.handler import WebSocketHandler

# monkey.patch_all()
# 初始化flask实例
# app = Flask(__name__, static_folder='./static', template_folder='')
app.config.update(DEBUG=True)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

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
    # query_msg = Host.query.all()
    # # list_msg = ListTool().dict_ls_reset_list(query_msg)
    # list_msg = ListTool().dict_ls_reset_dict(query_msg)
    # # host_title = ['id', '端口', 'ip地址', '密码', '名称', '登录用户', '组名']
    # host_title = ['id', '名称', 'ip地址', '端口', '登录用户', '组名', '操作']
    #
    # user_count = User2.query.count()
    # server_count = Host.query.count()
    # host_group = Host.query.with_entities(Host.group).all()
    # group_count = len(ListTool().list_rep_gather(host_group))
    # data = {
    #     'user_count': user_count,
    #     'server_count': server_count,
    #     'group_count': group_count
    # }
    # dir1 = LocalDirList().cmdlist_shell(DEFAULT_DIR1_PATH)
    # server_ip = ServerList().server_user
    # server_group = ServerList().server_group
    # return render_template('static/index.html', dir1=dir1, server_ip=server_ip, server_group=server_group, **data, hostls=list_msg, host_title=host_title)


# 这里是登录用户接口分割线 --------------------------------------------------------------------------------------------
@app.route('/account/login_dl', methods=['GET', 'POST'])
def login_dl():
    orange = UserLogin()
    return orange.login_dl()


@app.route('/account/chk_username', methods=['GET', 'POST'])
def chk_username():
    orange = CheckUser()
    return orange.check()


@app.route('/mail/send_user_mail', methods=['GET', 'POST'])
def send_user_mail():
    orange = CheckMail()
    return orange.send()


@app.route('/mail/send_mail', methods=['GET', 'POST'])
def send_mail():
    orange = OrangeMailApi()
    return orange.send()


@app.route('/account/com_register', methods=['GET', 'POST'])
def com_register():
    orange = UserRegister()
    return orange.register()


# 用户登录日志
@app.route('/account/login/logs', methods=['GET', 'POST'])
def acc_login_logs():
    orange = LoginLogs()
    return orange.get_login_logs()


@app.route('/account/login/date', methods=['GET', 'POST'])
def acc_login_date():
    orange = LoginLogs()
    return orange.get_date_logs()


@app.route('/server/group/cmd', methods=['GET', 'POST'])
def group_cmd():
    orange = GroupCmd()
    return orange.sh_cmd


# 这里是页面用户接口分割线 --------------------------------------------------------------------------------------------
@app.route('/server/acc/user/list', methods=['GET', 'POST'])
def acc_user_list():
    orange = AccUserList()
    return orange.sys_user_list


@app.route('/server/acc/user/list_all', methods=['GET', 'POST'])
def acc_user_list_all():
    orange = AccUserList()
    return orange.sys_user_list_all


@app.route('/server/acc/user/add', methods=['GET', 'POST'])
def acc_user_add():
    orange = AccUserAdd()
    return orange.host_add


@app.route('/server/acc/user/update', methods=['GET', 'POST'])
def acc_user_update():
    orange = AccUserUpdate()
    return orange.update


@app.route('/server/acc/user/del', methods=['GET', 'POST'])
def acc_user_del():
    orange = AccUserDel()
    return orange.host_del


# 这里是系统用户接口分割线 --------------------------------------------------------------------------------------------
@app.route('/server/sys/user/list', methods=['GET', 'POST'])
def sys_user_list():
    orange = SysUserList()
    return orange.sys_user_list


@app.route('/server/sys/user/list_all', methods=['GET', 'POST'])
def sys_user_list_all():
    orange = SysUserList()
    return orange.sys_user_list_all


@app.route('/server/sys/user/add', methods=['GET', 'POST'])
def sys_user_add():
    orange = SysUserAdd()
    return orange.host_add


@app.route('/server/sys/user/update', methods=['GET', 'POST'])
def sys_user_update():
    orange = SysUserUpdate()
    return orange.update


@app.route('/server/sys/user/del', methods=['GET', 'POST'])
def sys_user_del():
    orange = SysUserDel()
    return orange.host_del


# 这里是资产主机接口分割线 --------------------------------------------------------------------------------------------
@app.route('/server/host/add', methods=['GET', 'POST'])
def server_add():
    orange = ServerAdd()
    return orange.host_add


@app.route('/server/host/update', methods=['GET', 'POST'])
def server_update():
    orange = ServerUpdate()
    return orange.update


@app.route('/server/host/del', methods=['GET', 'POST'])
def server_del():
    orange = ServerDel()
    return orange.host_del


@app.route('/server/host/cmd', methods=['GET', 'POST'])
def server_cmd():
    orange = ServerCmd2()
    return orange.sh_cmd


@app.route('/server/host/list_all', methods=['GET', 'POST'])
def host_list_all():
    orange = ServerList()
    return orange.server_list_all


@app.route('/server/host/list', methods=['GET', 'POST'])
def host_list():
    orange = ServerList()
    return orange.server_list


@app.route('/server/host/list_page', methods=['GET', 'POST'])
def host_list_page():
    orange = ServerList()
    return orange.server_list_page


@app.route('/server/group_list', methods=['GET', 'POST'])
def group_list():
    orange = GroupList()
    return orange.server_list


@app.route('/server/count_list_all', methods=['GET', 'POST'])
def count_list():
    orange = CountList()
    return orange.server_count_all


@app.route('/server/host_list_cmd', methods=['GET', 'POST'])
def server_list_cmd():
    orange = ServerListCmd()
    return orange.sh_list_cmd


# 这里是资产组接口分割线 --------------------------------------------------------------------------------------------
@app.route('/server/host/group/list', methods=['GET', 'POST'])
def host_group_list():
    orange = AccGroupList()
    return orange.group_list


@app.route('/server/host/group/name_list', methods=['GET', 'POST'])
def host_group_name_list():
    orange = AccGroupList()
    return orange.group_name_list


@app.route('/server/host/group/list_all', methods=['GET', 'POST'])
def host_group_list_all():
    orange = AccGroupList()
    return orange.group_list_all


@app.route('/server/host/group/add', methods=['GET', 'POST'])
def host_group_add():
    orange = AccGroupAdd()
    return orange.host_add


@app.route('/server/host/group/update', methods=['GET', 'POST'])
def host_group_update():
    orange = AccGroupUpdate()
    return orange.update


@app.route('/server/host/group/del', methods=['GET', 'POST'])
def host_group_del():
    orange = AccGroupDel()
    return orange.host_del


@app.route('/server/file/put', methods=['GET', 'POST'])
def server_file():
    orange = ServerScript()
    return orange.sh_script()


# 这里是本地执行接口分割线 -------------------------------------------------------------------------------------
@app.route('/local/dir/group', methods=['GET', 'POST'])
def local_dir_group():
    orange = LocalDirList()
    return jsonify({'group_dir_msg': orange.cmdlist_shell(DEFAULT_DIR1_PATH)})


@app.route('/local/dir/project', methods=['GET', 'POST'])
def local_dir_project():
    orange = LocalDirList(DEFAULT_DIR1_PATH, DEFAULT_DIR2_PATH)
    return orange.getdir1()


@app.route('/local/rsync', methods=['GET', 'POST'])
def rcs():
    orange = LocalDirList(DEFAULT_DIR1_PATH, DEFAULT_DIR2_PATH, RSYNC_SHELL_CMD)
    return orange.getdir2()


@app.route('/local/sum', methods=['GET', 'POST'])
def data_sum():
    orange = DataSumAll()
    return orange.get_sum()


@app.route('/local/data', methods=['GET', 'POST'])
def data_list():
    orange = DataList()
    return orange.get_list()


if __name__ == "__main__":
    # app.run(host='0.0.0.0',port=28000)
    args = sta_cs()
    host = args.host
    port = args.port
    app.run(host=host, port=port)
    # http_server = WSGIServer((host,port),app,handler_class=WebSocketHandler)
    # http_server.serve_forever()
