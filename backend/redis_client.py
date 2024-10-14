from flask_session import Session
import redis
from config import *


class RedisConnectionPool():
    def __init__(self, db=0):
        self.pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=db)

    def getClient(self):
        return redis.StrictRedis(connection_pool=self.pool)


redis_pool = RedisConnectionPool()
redis_job_pool = RedisConnectionPool(3)


def createRedisClient(db=0):
    client = redis_pool.getClient()
    return client


def createRedisJobClient():
    return redis_job_pool.getClient()


def InitRedisDB(app):
    app.config['SECRET_KEY'] = SECRET_KEY

    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = False
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'

    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_PERMANENT'] = False

    app.config['PERMANENT_SESSION_LIFETIME'] = 7200 # 非永久cookie的过期时间，仅当 SESSION_PERMANENT = False 时生效
    app.config['SESSION_REDIS'] = createRedisClient(0)
    Session(app)

"""
set(name, value, ex=None, px=None, nx=False, xx=False)
在 Redis 中设置值，默认，不存在则创建，存在则修改。
参数：
ex - 过期时间（秒）
px - 过期时间（毫秒）
nx - 如果设置为True，则只有name不存在时，当前set操作才执行
xx - 如果设置为True，则只有name存在时，当前set操作才执行
"""
