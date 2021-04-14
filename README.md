# OrangeServer

#### 介绍
用python flask jinja2和ajax前后端交互实现的运维管理平台，同时使用gevent实现了进程异步处理请求

#### 软件架构
软件架构说明: 管理界面，ansible批量执行命令，管理docker等功能待开发


#### 安装教程

1.  必须为python3以上环境
2.  pip3 install -r requirements.txt
3.  python3 app_run.py --host 主机ip或者0.0.0.0 --port 端口号

#### 使用说明

1.  注册界面展示
2.  ![ys1](./pic/zc.png)
3.  登录界面展示
4.  ![ys1](./pic/dl.png)
5.  同步代码功能,点击列表内仓库组和项目同步代码到线上，仅限linux环境
6.  ![ys1](./pic/ys.png)
7.  ![ys1](./pic/ys1.png)
8.  ![ys1](./pic/ys2.png)

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request
