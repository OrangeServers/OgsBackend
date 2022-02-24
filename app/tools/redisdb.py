import redis
from app.conf.conf import REDIS_CONF


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
        self.Pool = redis.ConnectionPool(host=self.host, port=self.port, db=10, max_connections=self.max_connections, decode_responses=True)
        self.conn = redis.StrictRedis(connection_pool=self.Pool)


if __name__ == "__main__":
    ords = ConnRedis(REDIS_CONF['host'], REDIS_CONF['port'])
    print(ords.conn.get('name'))
