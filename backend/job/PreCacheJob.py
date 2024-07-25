from configs import scheduler, REDISLOCK
from database import User
from service import userService
from redis_client import createRedisJobClient
import json


class PreCacheJob(object):
    """
    docstring for PreCacheJob
    每天执行，预热推荐用户
    优化点：
        重点用户
        分布式锁    √
    """
    def __init__(self):
        self.mainUserList = [3]
        self.redisClient = createRedisJobClient()

    def doCacheRecommendUser(self):
        acquired_lock = False
        try:
            acquired_lock = REDISLOCK.acquire(blocking=False)
            if acquired_lock:
                print('我抢锁成功啦！', flush=True)
                for userId in self.mainUserList:
                    userPage = userService().page(10, 1)
                    redisKey = f'paopao:user:recommend:{userId}'
                    print('定时任务开启，自动设置推荐缓存', flush=True)
                    self.redisClient.set(redisKey, json.dumps(userPage), ex=30000)
            else:
                print('我抢锁失败了....', flush=True)
        except Exception as e:
            print(f"分布式锁业务逻辑执行失败: {e}", flush=True)
        finally:
            if acquired_lock:
                REDISLOCK.release()
                print('释放分布式锁成功', flush=True)

item = PreCacheJob()
