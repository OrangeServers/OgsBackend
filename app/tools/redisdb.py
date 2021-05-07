import redis
from app.conf.conf_test import REDIS_CONF


# 操作redis数据库
class ConnRedis:
    """
    host-->redis的ip地址,str类型
    port-->redis的端口,int类型
    max_connections-->连接最大超时时间,int类型
    """
    def __init__(self, host, port, max_connections=10):
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.Pool = redis.ConnectionPool(host=self.host, port=self.port, db=10, max_connections=self.max_connections)
        self.redis_conn = redis.Redis(connection_pool=self.Pool, decode_responses=True)

    def get_red(self, key):
        """
        key-->需要查询的key,str类型
        """
        try:
            msg = self.redis_conn.get(key).decode()
            return msg
        except AttributeError:
            return None

    def set_red(self, key, value):
        """
        key-->需要写入的key,str类型
        value-->需要写入的value,str类型
        """
        msg = self.redis_conn.set(key, value)
        return msg

    def exp_red(self, key, time):
        """
        key-->需要更改的key,str类型
        time-->需要设定的key过期时间,int类型
        """
        msg = self.redis_conn.expire(key, time)
        return msg


if __name__ == "__main__":
    cn_red = ConnRedis(REDIS_CONF['host'],REDIS_CONF['port'])
    cn_red.get_red('name')