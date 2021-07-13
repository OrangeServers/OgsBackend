from sqlalchemy import Column, String, INTEGER, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.conf.conf_test import MYSQL_CONF

"""
    说明:
        @ 这里的create_engine进行的操作是创建数据库连接,填写参数格式如下: 
        @ '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
        @ 这里使用了.format函数,这就是个占位符,在format中按顺序填写就好,也可以指定编号比如{1}
"""
engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(MYSQL_CONF['user'], MYSQL_CONF['password'],
                                                               MYSQL_CONF['host'], MYSQL_CONF['port'],
                                                               MYSQL_CONF['dbname']))

"""
    说明:
        @ 这里的sessionmaker是一个工厂类,按照我们创建的engine绑定了数据库引擎
        @ 当我们使用这个Session的时候都会创建一个绑定引擎的Session,通过Session操作数据库
"""
DBSession = sessionmaker(bind=engine)

# 创建一个父类数据库
Base = declarative_base()

"""
    说明:
        @ 以下代码会创建flask数据库中user表的映射关系
        通过继承父类,指定字段类型表名将会建立映射关系

"""


class User(Base):
    __tablename__ = 't_user'  # 指定表名字为 user
    # 主键id, 自增, Integer类型
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    # userName字段 varchar类型 限制45 不为空
    name = Column(String(10), nullable=False)
    # passWord字段, varchar类型 限制45 不为空
    password = Column(String(45), nullable=False)
    mail = Column(String(45), nullable=False)
