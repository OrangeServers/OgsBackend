from flask import request
from Flask_App_Settings import app
from app.sqldb.SqlAlchemyDB import t_host
from app.tools.basesec import BaseSec
# pip install gevent-websocket导入IO多路复用模块
from geventwebsocket.handler import WebSocketHandler  # 提供WS（websocket）协议处理
from geventwebsocket.server import WSGIServer  # websocket服务承载
# WSGIServer导入的就是gevent.pywsgi中的类
# from gevent.pywsgi import WSGIServer
from geventwebsocket.websocket import WebSocket  # websocket语法提示


import paramiko
import time
import json

hostname = '10.0.1.199'
port = 22
username = 'root'
password = 'jlb123'
timeout = 10


class ParSsh:
    def __init__(self, p_host, p_port, p_user, p_psw):
        self.host = p_host
        self.port = p_port
        self.user = p_user
        self.psw = p_psw
        self.trans = paramiko.Transport((self.host, self.port)) # 【坑1】 如果你使用 paramiko.SSHClient() cd后会回到连接的初始状态
        self.trans.start_client()
        self.trans.auth_password(username=self.user, password=self.psw)
        self.channel = self.trans.open_session()
        self.channel.settimeout(10)
        # 获取一个终端
        self.channel.get_pty()
        # 激活器
        self.channel.invoke_shell()

    def test_paramiko_interact(self, cmd):

        # 发送要执行的命令
        lt_msg = ''
        self.channel.send(cmd)  # 【坑2】 如果你使用 sh ./study_shell.sh\r 可能会出现 [: 11: y: unexpected operator 错误
        # 回显很长的命令可能执行较久，通过循环分批次取回回显
        while True:
            # time.sleep(0.2)
            # msg = self.channel.recv(1024)
            # return msg.decode()
            time.sleep(0.2)
            msg = self.channel.recv(1024)
            if len(msg) >= 1024:
                # print(len(msg))
                lt_msg += msg.decode('utf-8')
                # print(lt_msg)
            elif len(msg) < 1024:
                lt_msg += msg.decode('utf-8')
                break
        return lt_msg


client_list = []


# @app.route('/websocket')
class OgsWebSocket:
    def __init__(self):
        self.bse = BaseSec()
        self.client_socket = request.environ.get('wsgi.websocket')  # type:WebSocket

    def web_ssh(self):
        try:
            # 第一次接收数据转dict，新建ssh连接并核对用户名密码
            msg_one_cli = self.client_socket.receive()
            # json转dict
            test1 = json.loads(msg_one_cli)
            print(type(test1), test1['hostname'])
            query_host_msg = t_host.query.filter_by(alias=test1['hostname']).first()
            query_msg = query_host_msg.__dict__
            # conn = ParSsh(hostname, port, username, password)
            # 根据客户端发送的用户名密码连接
            conn = ParSsh(query_msg['host_ip'], query_msg['host_port'], query_msg['host_user'], self.bse.base_de(query_msg['host_password']))
            # print(len(client_list), client_list)
            while 1:
                msg_from_cli = self.client_socket.receive()
                # print(msg_from_cli)
                msg = conn.test_paramiko_interact(msg_from_cli)
                res_msg = msg[msg.find('\r\n')+2:]
                print(res_msg)
                self.client_socket.send(res_msg)
        except TypeError:
            print('val is none')
        except paramiko.ssh_exception.SSHException:
            print(1)
            self.client_socket.send('Unable to connect to {}: [Errno 110] Connection timed out'.format(query_msg['host_ip']))
            return {'status': 1}


if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 8014), application=app, handler_class=WebSocketHandler)
    http_server.serve_forever()