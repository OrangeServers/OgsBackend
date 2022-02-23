import os

# 测试环境配置
DEFAULT_DIR1_PATH = 'ls /data'
DEFAULT_DIR2_PATH = "ls /data/%s"
RSYNC_SHELL_CMD = "/usr/bin/rsync -av /data/%s/%s /data/tmp/"

DEFAULT_DATA_DIR = os.getcwd() + '/data'     # 服务的数据目录，默认当前目录的data
DEFAULT_IMG_DIR = DEFAULT_DATA_DIR + '/img/'
DEFAULT_PTU_DIR = DEFAULT_DATA_DIR + '/file/'
DEFAULT_KEY_DIR = DEFAULT_DATA_DIR + '/key/'

# 邮件配置
MAIL_CONF = {
    'form_mail': 'you mail name',         # 邮箱账号
    'password': 'you mail password',        # 邮箱密码 这里通过smtp登录需要去邮箱获取授权码，而非密码
    'smtp_server': 'you mail smtp server'    # 邮箱地址 例如163的 stmp.163.com
}

# mysql配置
MYSQL_CONF = {
    'dbname': 'you dababase name',      # 数据库名
    'user': 'you user name',           # 数据库用户名
    'password': 'you password',       # 数据库用户密码
    'host': 'you db host ip',        # 数据库地址
    'port': 3306                    # 数据库端口号
}

# redis配置
REDIS_CONF = {
    'host': 'you redis ip',           # redis地址
    'port': 6379                    # redis端口号
}

# 文件路径配置
FILE_CONF = {
    'image_path': DEFAULT_DATA_DIR + '/img/',
    'file_path': DEFAULT_DATA_DIR + '/file/',
    'file_path2': DEFAULT_DATA_DIR + '/file',
    'key_path': DEFAULT_DATA_DIR + '/key/'
}
