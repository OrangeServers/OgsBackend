import datetime
from app.sqldb.SqlAlchemySettings import db
from app.tools.SqlListTool import ListTool


class t_host(db.Model):
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
    alias = db.Column(db.String(30), nullable=False)
    # userName字段 varchar类型 限制45 不为空
    host_user = db.Column(db.String(25), nullable=False)
    # passWord字段, varchar类型 限制45 不为空
    host_password = db.Column(db.String(25), nullable=False)
    agreement = db.Column(db.String(10), nullable=False)
    nums = db.Column(db.INT, nullable=False)
    remarks = db.Column(db.String(30), nullable=True)


class t_acc_user(db.Model):
    __tablename__ = 't_acc_user'  # 指定表名字为 user
    # 主键id, 自增, Integer类型
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    alias = db.Column(db.String(24), nullable=False)
    # userName字段 varchar类型 限制45 不为空
    name = db.Column(db.String(24), nullable=False)
    # passWord字段, varchar类型 限制45 不为空
    password = db.Column(db.String(24), nullable=False)
    usrole = db.Column(db.String(10), nullable=False)
    mail = db.Column(db.String(24), nullable=False)
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


class t_acc_group(db.Model):
    __tablename__ = 't_acc_group'  # 指定表名字为 user
    # 主键id, 自增, Integer类型
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    # userName字段 varchar类型 限制45 不为空
    name = db.Column(db.String(25), nullable=False)
    # passWord字段, varchar类型 限制45 不为空
    nums = db.Column(db.INT, nullable=False)
    remarks = db.Column(db.String(30), nullable=True)


class t_login_log(db.Model):
    __tablename__ = 't_login_log'  # 指定表名字为 user
    # 主键id, 自增, Integer类型
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    login_name = db.Column(db.String(30), nullable=False)
    # userName字段 varchar类型 限制45 不为空
    login_nw_ip = db.Column(db.String(20), nullable=False)
    # passWord字段, varchar类型 限制45 不为空
    login_gw_ip = db.Column(db.String(20), nullable=True)
    login_gw_cs = db.Column(db.String(20), nullable=True)
    login_agent = db.Column(db.String(20), nullable=False)
    login_status = db.Column(db.String(255), nullable=False)
    login_reason = db.Column(db.String(30), nullable=True)
    login_time = db.Column(db.TIMESTAMP, nullable=False)


class t_command_log(db.Model):
    __tablename__ = 't_command_log'  # 指定表名字为 user
    # 主键id, 自增, Integer类型
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    com_name = db.Column(db.String(30), nullable=False)
    # userName字段 varchar类型 限制45 不为空
    com_type = db.Column(db.String(30), nullable=False)
    # passWord字段, varchar类型 限制45 不为空
    com_info = db.Column(db.String(255), nullable=False)
    com_host = db.Column(db.String(255), nullable=False)
    com_status = db.Column(db.String(10), nullable=False)
    com_reason = db.Column(db.String(255), nullable=True)
    com_time = db.Column(db.TIMESTAMP, nullable=False)


class t_auth_host(db.Model):
    __tablename__ = 't_auth_host'  # 指定表名字为 user
    # 主键id, 自增, Integer类型
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    # userName字段 varchar类型 限制45 不为空
    name = db.Column(db.String(25), nullable=False)
    # passWord字段, varchar类型 限制45 不为空
    user = db.Column(db.String(255), nullable=True)
    user_group = db.Column(db.String(255), nullable=True)
    host_group = db.Column(db.String(255), nullable=True)
    remarks = db.Column(db.String(255), nullable=True)


class t_line_chart(db.Model):
    __tablename__ = 't_line_chart'  # 指定表名字为 user
    # 主键id, 自增, Integer类型
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    login_count = db.Column(db.INT, nullable=False, default=0)
    user_count = db.Column(db.INT, nullable=False, default=0)
    chart_date = db.Column(db.DATE, nullable=False)


class t_settings(db.Model):
    __tablename__ = 't_settings'  # 指定表名字为 user
    # 主键id, 自增, Integer类型
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, default=0)
    login_time = db.Column(db.INT, nullable=False, default=3)
    register_status = db.Column(db.String(5), nullable=False, default="on")
    color_matching = db.Column(db.String(10), nullable=False, default="black")


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

    res_host = Host.query.offset(5).limit(5).all()
    for host_ls in res_host:
        print(host_ls.id)

    print('需要的-----------------')
    group_count = Host.query.with_entities(Host.group).all()
    print(t_group.query.with_entities(t_group.name).all())
    print(list_tool.list_rep_gather(group_count))

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
    # 多条件查询
    login_query = t_login_log.query.filter_by(logintime='login_time', loginname='username').first()
    query_msg = t_login_log.query.filter(t_login_log.login_time.like("%2021-05-11%"),
                                         db.cast(t_login_log.login_time, db.DATE)).all()
    # 时间段查询
    query_msg = t_login_log.query.filter(t_login_log.login_time >= '2021-05-11 00:00:00').filter(
        t_login_log.login_time <= '2021-05-12 00:00:00').order_by(t_login_log.login_time.desc()).all()

    # 一个字段多值查询
    test = Host.query.filter(Host.group.in_([1, 2, 3])).all()
