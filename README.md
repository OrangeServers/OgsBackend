# OgsBackend

### 简介
orangeservers的后端项目，整体部署和展示文档在[OgsDocument](https://github.com/OrangeServers/OgsDocument)

项目使用python3+flask编写

### 部署

```shell
# 该项目用到了python3环境，redis，mysql，nginx，需要提前安装
# 下载后端服务压缩包
wget http://58.135.83.162:19612/ogsbackend/v1.0/orangeservers_v1.0.tar.gz

# 解压orangeserver压缩包，导入数据文件
tar -xf orangeservers_v1.0.tar.gz && cd orangeservers
# 安装依赖库
pip3 install -r requirements.txt
# 你的数据库地址用户名和密码
mysql -uxxx -pxxx -hx.x.x.x
mysql> create database orange;
# 导入数据文件
mysql -uxxx -pxxx -hx.x.x.x orange < mysqldir/orange.sql

# 修改后端配置文件
cp app/conf/conf_exapmple.py app/conf/conf.py
vim app/conf/conf.py
# 一般只需要修改这三处即可
# 邮件配置
MAIL_CONF = {
    'form_mail': 'you mail name',         # 邮箱账号 不用邮箱功能也可以不配置
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

# 配置python解释器路径,自行修改
vim start.sh
python3_path='python3'   # 修改值为解释器全路径

# 启动服务，默认有两个端口 28000和8888
chmod +x start.sh
./start start
```

