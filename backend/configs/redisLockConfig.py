import redis_lock
from redis_client import createRedisClient
from redis_client import createRedisJobClient

conn = createRedisJobClient()
REDISLOCK = redis_lock.Lock(
    conn,
    'paopao:precachejob:docache:lock',
    expire=3600,
    auto_renewal=True)

def JoinTeamLock(teamId):
    return redis_lock.Lock(
        conn,
        f'paopao:joinTeam:lock:{teamId}',
        expire=60,
        auto_renewal=True)
