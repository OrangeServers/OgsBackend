# -*- coding=utf8 -*-
from flask import render_template
from Flask_App_Settings import *
from datetime import timedelta
import argparse
from app.foo.user.decorator import wrapper
from app.foo.local.Basics import CountList
from app.foo.property.ServerManagement import ServerAdd, ServerList, ServerCmd2, ServerListCmd, ServerDel, GroupCmd, GroupList, ServerUpdate
from app.foo.user.AccUser import UserLogin, CheckUser, CheckMail, UserRegister, User_List
from app.foo.property.SysUser import SysUserList, SysUserAdd, SysUserUpdate, SysUserDel
from app.conf.conf_test import *
from app.foo.local.LocalShell import LocalDirList
from app.sqldb.SqlAlchemyDB import User2, Host
from app.foo.mail.MailApi import OrangeMailApi
from app.tools.SqlListTool import ListTool

# from gevent import monkey
# from gevent.pywsgi import WSGIServer
# from geventwebsocket.handler import WebSocketHandler

# monkey.patch_all()
# 初始化flask实例
# app = Flask(__name__, static_folder='./static', template_folder='')
app.config.update(DEBUG=True)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

# 赋予session值的密钥
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
@wrapper
def index():

    query_msg = Host.query.all()
    # list_msg = ListTool().dict_ls_reset_list(query_msg)
    list_msg = ListTool().dict_ls_reset_dict(query_msg)
    # host_title = ['id', '端口', 'ip地址', '密码', '名称', '登录用户', '组名']
    host_title = ['id', '名称', 'ip地址', '端口', '登录用户', '组名', '操作']

    user_count = User2.query.count()
    server_count = Host.query.count()
    host_group = Host.query.with_entities(Host.group).all()
    group_count = len(ListTool().list_rep_gather(host_group))
    data = {
        'user_count': user_count,
        'server_count': server_count,
        'group_count': group_count
    }
    dir1 = LocalDirList().cmdlist_shell(DEFAULT_DIR1_PATH)
    server_ip = ServerList().server_user
    server_group = ServerList().server_group
    return render_template('static/index.html', dir1=dir1, server_ip=server_ip, server_group=server_group, **data, hostls=list_msg, host_title=host_title)


@app.route('/account/acc_user_list_all', methods=['GET', 'POST'])
def acc_user_list_all():
    ul = User_List()
    return ul.acc_user_list_all


@app.route('/account/group_list_all', methods=['GET', 'POST'])
def group_list_all():
    ul = User_List()
    return ul.group_list_all


@app.route('/account/login_dl', methods=['GET', 'POST'])
def login_dl():
    login = UserLogin()
    return login.login_dl()


@app.route('/account/chk_username', methods=['GET', 'POST'])
def chk_username():
    chkuser = CheckUser()
    return chkuser.check()


@app.route('/mail/send_user_mail', methods=['GET', 'POST'])
def send_user_mail():
    email = CheckMail()
    return email.send()


@app.route('/mail/send_mail', methods=['GET', 'POST'])
def send_mail():
    send = OrangeMailApi()
    return send.send()


@app.route('/account/com_register', methods=['GET', 'POST'])
def com_register():
    zhuce = UserRegister()
    return zhuce.register()


@app.route('/server/host_add', methods=['GET', 'POST'])
def server_add():
    seradd = ServerAdd()
    return seradd.host_add


@app.route('/server/host_update', methods=['GET', 'POST'])
def server_update():
    serupdate = ServerUpdate()
    return serupdate.update


@app.route('/server/host_del', methods=['GET', 'POST'])
def server_del():
    serdel = ServerDel()
    return serdel.host_del


@app.route('/server/host_cmd', methods=['GET', 'POST'])
def server_cmd():
    # sercmd = ServerCmd()
    # return sercmd.sh_cmd
    sercmd = ServerCmd2()
    return sercmd.sh_cmd


@app.route('/server/group_cmd', methods=['GET', 'POST'])
def group_cmd():
    gopcmd = GroupCmd()
    return gopcmd.sh_cmd


@app.route('/server/sys_user_list_all', methods=['GET', 'POST'] )
def sys_user_list_all():
    sl = SysUserList
    return sl.sys_user_list_all


@app.route('/server/host_list_all', methods=['GET', 'POST'] )
def host_list_all():
    serlit = ServerList()
    return serlit.server_list_all


@app.route('/server/host_list', methods=['GET', 'POST'] )
def host_list():
    serlit = ServerList()
    return serlit.server_list


@app.route('/server/group_list', methods=['GET', 'POST'] )
def group_list():
    gl = GroupList()
    return gl.server_list


@app.route('/server/count_list_all', methods=['GET', 'POST'] )
def count_list():
    sl = CountList()
    return sl.server_count_all


@app.route('/server/host_list_cmd', methods=['GET', 'POST'] )
def server_list_cmd():
    sercmd = ServerListCmd()
    return sercmd.sh_list_cmd


@app.route('/local/getdir', methods=['GET', 'POST'])
def getdir():
    dir = LocalDirList(DEFAULT_DIR1_PATH, DEFAULT_DIR2_PATH)
    return dir.getdir1()


@app.route('/local/rsync', methods=['GET', 'POST'])
def rcs():
    dir = LocalDirList(DEFAULT_DIR1_PATH, DEFAULT_DIR2_PATH, RSYNC_SHELL_CMD)
    return dir.getdir2()


if __name__ == "__main__":
    # app.run(host='0.0.0.0',port=28000)
    args = sta_cs()
    host = args.host
    port = args.port
    app.run(host=host, port=port)
    # http_server = WSGIServer((host,port),app,handler_class=WebSocketHandler)
    # http_server.serve_forever()
