from flask_sqlalchemy import SQLAlchemy
from Flask_App_Settings import app
from app.conf.conf_test import MYSQL_CONF
from app.tools.SqlListTool import ListTool

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://{}:{}@{}:{}/{}".format(MYSQL_CONF['user'],
                                                                                MYSQL_CONF['password'],
                                                                                MYSQL_CONF['host'], MYSQL_CONF['port'],
                                                                                MYSQL_CONF['dbname'])
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)


class User2(db.Model):
    __tablename__ = 't_user'  # 指定表名字为 user
    # 主键id, 自增, Integer类型
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    # userName字段 varchar类型 限制45 不为空
    name = db.Column(db.String(10), nullable=False)
    # passWord字段, varchar类型 限制45 不为空
    password = db.Column(db.String(45), nullable=False)
    mail = db.Column(db.String(45), nullable=False)


class Host(db.Model):
    __tablename__ = 't_host'  # 指定表名字为 user
    # 主键id, 自增, Integer类型
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    # alias字段 varchar类型 限制25 不为空
    alias = db.Column(db.String(25), nullable=False)
    # host_ip字段, varchar类型 限制16 不为空
    host_ip = db.Column(db.VARCHAR(16), nullable=False)
    # host_port字段, int类型 限制4 不为空
    host_port = db.Column(db.INT, nullable=False)
    # host_user字段, varchar类型 限制20 不为空
    host_user = db.Column(db.VARCHAR(20), nullable=False)
    # host_password字段, varchar类型 限制20 不为空
    host_password = db.Column(db.String(20), nullable=False)
    # group字段, varchar类型 限制20 可为空
    group = db.Column(db.String(20), nullable=True)


class t_sys_user(db.Model):
    __tablename__ = 't_sys_user'  # 指定表名字为 user
    # 主键id, 自增, Integer类型
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    # userName字段 varchar类型 限制45 不为空
    host_user = db.Column(db.String(25), nullable=False)
    # passWord字段, varchar类型 限制45 不为空
    host_password = db.Column(db.String(25), nullable=False)
    agreement = db.Column(db.String(10), nullable=False)
    nums = db.Column(db.INT, nullable=False)
    remarks = db.Column(db.String(30), nullable=True)


class t_group(db.Model):
    __tablename__ = 't_group'  # 指定表名字为 user
    # 主键id, 自增, Integer类型
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    # userName字段 varchar类型 限制45 不为空
    name = db.Column(db.String(25), nullable=False)
    # passWord字段, varchar类型 限制45 不为空
    nums = db.Column(db.INT, nullable=False)
    remarks = db.Column(db.String(30), nullable=True)


if __name__ == '__main__':
    list_tool = ListTool()
    results = User2.query.all()
    print(results)
    res = list_tool.dict_ls_reset_list(results)
    print(res)
    results2 = User2.query.with_entities(User2.id).all()
    print(results2)
    results3 = list_tool.list_gather(results2)
    print(results3)

    res_host = Host.query.all()
    for host_ls in res_host:
        print(host_ls.id)

    print('-----------------')
    group_count = Host.query.with_entities(Host.group).all()
    print(len(list_tool.list_rep_gather(group_count)))

    print('-----------------')
    group_select = []
    group_list = Host.query.filter_by(group='default').all()
    host_ip_list = []
    for groups in group_list:
        group_dict = groups.__dict__
        print(group_dict)
        msg = ListTool.dict_reset_list(groups)
        group_select.append(msg)
        host_ip_list.append(group_dict['host_ip'])
    print(Host.query.filter_by(group='default').count())
    print(ListTool.dict_ls_reset_list(group_list))
    print(host_ip_list)
