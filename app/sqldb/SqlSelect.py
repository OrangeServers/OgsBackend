from app.sqldb.SqlAlchemyConf import DBSession, User

# 实例化session对象
session = DBSession()
"""
    说明:
        @ query(User).all() 函数中, query()的参数是你要查找的表的映射对象,也就是SqlAlchemyConf文件下的 class User对象
        @ all的意思就是全部,所以第一个函数是查询所有

        @ query(User).count()   查询记录条数总数
        @ query(User).filter_by(userName='jack6').first() : 查询用户名为 jack6的第一个用户 返回单个对象 如果写all返回的是list

        @ query(User).slice(0, 3): 查询三条数据,slice应用在分页查询中
        @ 分页的使用参考我这篇文章 :https://blog.csdn.net/weixin_44232093/article/details/100017742
"""


def query_user():
    user__all = session.query(User).all()
    for user in user__all:
        print("用户名: {}      密码: {}".format(user.name, user.password))
        print(user.__dict__)

    count = session.query(User).count()
    print("总记录条数为: {}".format(count))

    first_name_eq_jack = session.query(User).filter_by(name='admin').one()
    # print("查询用户名为 admin的用户的id为: {}".format(first_name_eq_jack.id))
    # print(first_name_eq_jack.password)
    res = list(first_name_eq_jack.__dict__.values())
    res.pop(0)
    print(res)

    user__slice = session.query(User).slice(0, 3)
    for slice in user__slice:
        print("分页查询三条的结果为: id为; {}     用户名为: {}".format(slice.id, slice.name))


if __name__ == '__main__':
    query_user()
