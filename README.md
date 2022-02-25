# OgsBackend

### 简介

orangeservers是一款开源的运维管理平台（开源堡垒机）

该项目是orangeserver v1.0的官方文档，安装，使用，部署文档将集中在此，项目的部分还在开发中

该项目orangeservers的后端项目，整体部署和展示文档在[OgsDocument](https://github.com/OrangeServers/OgsDocument)

项目使用python3+flask编写

### 功能概述

- 注册
- 登录
- 资产管理
- 用户管理
- 批量命令
- 批量脚本（目前只支持shell）
- web终端
- 容器管理（还在开发中，暂无功能）
- 日志审计
- 权限管理
- 定时任务（可批量）
- 文件传输（暂时只实现文件上传到后端服务器，文件上传到资产机器还在开发中）
- 系统设置（功能较少，后续完善）

### 部署

查看不了图片或者克隆慢可以去gitee的仓库，[这是地址](https://gitee.com/xuwei777/OgsBackend)

```shell
# 该项目用到了python3环境，redis，mysql，nginx，需要提前安装
# 克隆OgsBackend安装包 国内环境克隆慢可以去gitee克隆
git clone https://github.com/OrangeServers/OgsBackend.git

# 也可以直接下载安装压缩包 wget  http://download.stisd.cn/ogsbackend/OgsBackend_v1.0.tar.gz
# 改名
mv OgsBackend orangeservers

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

