import pymysql, itertools


# 用于使用pymysql操作数据库
class ConnMysql:
    """
    dbname-->数据库库名,str类型
    user-->数据库用户名,str类型
    password-->数据库密码,str类型
    host-->数据库ip,str类型
    port-->数据库端口,int类型
    """
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = pymysql.connect(db=self.dbname,user=self.user,password=self.password,host=self.host,port=self.port,charset='utf8')

    def sel_sql(self, sql):
        """
        sql-->查询数据的sql语句，返回值为列表里带元组,str类型
        """
        cursor = self.connection.cursor()
        cursor.execute(sql)
        # result = cursor.fetchone()
        sqlmsg= list(cursor.fetchall())
        cursor.close()
        return sqlmsg
        # self.connection.close()

    def sel_dl_sql(self, sql):
        """
        sql-->查询数据的sql语句，返回值为整合的单列表,str类型
        """
        cursor = self.connection.cursor()
        cursor.execute(sql)
        # result = cursor.fetchone()
        result = cursor.fetchall()
        sqlmsg = (list(itertools.chain.from_iterable(set(result))))
        cursor.close()
        return sqlmsg

    def set_sql(self, sql):
        """
        sql-->插入或更新数据的sql语句,str类型
        """
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

    def czgsh(self,czxx):
        gsh = ["船只id: ","厂商: ","船只: ","中文翻译: ","官网价格: ","游戏币价格: ","船员: ","货物: ","最大速度: ","HP: ","护盾","DPS: ","导弹: ","量子速度: ","量子范围: "]
        xq = ("\n".join([i[0]+str(i[1]) for i in zip(gsh,czxx)]))
        return xq


if __name__ == "__main__":
    cnsql = ConnMysql()
    sqls = cnsql.sel_sql("select 厂商 from tb_tmp1;")
    xinxi = (','.join(sqls))
    print("船只厂商信息如下: %s" % (xinxi))
