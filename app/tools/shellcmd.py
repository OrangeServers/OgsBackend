import paramiko


# 远程操作linux服务器
class RemoteConnection:
    def __init__(self, host, port, username, password):
        """
        host-->远程连接的主机ip,str类型
        port-->远程连接的主机ssh端口,int类型
        username-->远程连接的主机用户名,str类型
        password-->远程连接的主机用户密码,str类型
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def ssh_cmd(self, command):
        """
        command-->需要执行的shell命令,str类型
        """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.host, port=self.port, username=self.username, password=self.password, timeout=3)
        stdin, stdout, stderr = ssh.exec_command(command)
        # stdin_msg = stdin.read()
        stdout_msg = stdout.read()
        stderr_msg = stderr.read()
        ssh.close()
        if stdout_msg.decode() == '':
            return stderr_msg.decode()
        elif stderr_msg.decode() == '':
            return stdout_msg.decode()

    def ssh_cmd_list(self, command_list):
        """
        command_list-->需要批量执行的shell命令,;list类型
        """
        for i in command_list:
            msg = self.ssh_cmd(i)
            return msg

    def put_file(self, form_path, to_path):
        """
        form_path-->从本地上传的文件路径;str类型
        to_path-->上传到对方服务器的文件路径;str类型
        """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.host, port=self.port, username=self.username, password=self.password, timeout=3)
        sftp_cilent = paramiko.SFTPClient.from_transport(ssh.get_transport())
        sftp_cilent.put(form_path, to_path)
        sftp_cilent.close()

    def put_file_list(self, form_path_list, to_path):
        """
        form_path_list-->从本地上传的文件路径;list类型
        to_path-->上传到对方服务器的文件路径;str类型
        """
        for i in form_path_list:
            self.put_file(i, to_path)


# 新增继承方法，待测试
class RemoteConnectionKey(RemoteConnection):
    def __init__(self, host, port, username, pkey):
        super(RemoteConnectionKey, self).__init__()
        """
        host-->远程连接的主机ip,str类型
        port-->远程连接的主机ssh端口,int类型
        username-->远程连接的主机用户名,str类型
        password-->远程连接的主机用户密码,str类型
        """
        self.host = host
        self.port = port
        self.username = username
        self.pkey = pkey

    def ssh_cmd(self, command):
        """
        command-->需要执行的shell命令,str类型
        """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        key = paramiko.RSAKey.from_private_key_file(self.pkey)
        ssh.connect(self.host, port=self.port, username=self.username, pkey=key, timeout=3)
        stdin, stdout, stderr = ssh.exec_command(command)
        # stdin_msg = stdin.read()
        stdout_msg = stdout.read()
        stderr_msg = stderr.read()
        ssh.close()
        if stdout_msg.decode() == '':
            return stderr_msg.decode()
        elif stderr_msg.decode() == '':
            return stdout_msg.decode()


if __name__ == '__main__':
    test_yw200 = RemoteConnection('10.0.1.200', 22, 'root', 'jlb123')
    test_yw200.ssh_cmd('hostname')
    ssh = paramiko.SSHClient()
    test_yw200.put_file('/data/tmp/1.txt', '/data/tmp/1.txt')
