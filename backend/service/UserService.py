from flask import session
from service.Base import base
from database import db, User
from utils import unionUserItem, AlgorithmUtils
from redis_client import createRedisClient
import json, time, os
from configs import UserConfig
from werkzeug.utils import secure_filename
from config import HOST, PORT


redisClient = createRedisClient()
algorithmUtils = AlgorithmUtils()
USER_LOGIN_STATE = UserConfig['USER_LOGIN_STATE']


class userService(base):
    def __init__(self):
        self.table = User

    def unifyItem(self, item):
        """
        Team ORM transilate to dict
        """
        return unionUserItem(item)

    def updateUser(self, user, loginUser):
        """
        更新用户信息，仅管理员和自己可修改,
        如果是管理员，可更新任意用户
        如果不是管理员，只允许更新当前用户信息
        user = 前端传入的需要修改的数据
        loginUser = 已登录的用户信息
        """
        userId = user.get('id', -1)

        if not self.OverrideIsAdmin(loginUser) and userId != loginUser['id']:
            return None
        oldUser = self.query().filter_by(id=userId).first()
        if not oldUser:
            return None

        for k, v in user.items():
            if k == 'tags':
                setattr(oldUser, k, json.dumps(v))
                loginUser[k] = v
            elif k != 'id' and hasattr(oldUser, k):
                setattr(oldUser, k, v)
                loginUser[k] = v

        db.session.commit()
        session[USER_LOGIN_STATE] = loginUser
        return True

    def page(self, pageSize, pageNum):
        array = []
        offset = (pageNum - 1) * pageSize
        users = self.query().order_by(
            User.id).limit(pageSize).offset(offset).all()
        for user in users:
            item = unionUserItem(user)
            array.append(item)
        return array

    def getMatchUserIdCache(self, userId):
        userIdCacheKey = f'match:user:{userId}'
        raw_list = redisClient.zrange(userIdCacheKey, 0, -1)
        return list(map(lambda x: int(x), raw_list))

    def matchUsers(self, num):
        """
        默认缓存20条，可在configs/UserConfig.py中配置
        todo:
            使用Redis 的 zset    √
                zset记录最匹配的userId
                key = 'match:user:{userId}', value = 'distance, matchedUserId'
                如果存在缓存，则获取所有的用户id，再按id从数据库中查询
                如果不存在缓存，则从数据库中进行全匹配，并设置redis缓存
            查询上有什么可以优化的点
                过滤空tags用户 √
                按更新时间排序
                User 表添加上次登录时间 lastLoginTime
            数据是否预热
        """
        result = {'msg': '', 'ret': 0, 'data': []}
        try:
            matchUsersCacheNum = UserConfig['matchUsersCacheNum']
            if num <= 0 or num > matchUsersCacheNum:
                result['msg'], result['ret'] = f'参数设置错误（num = 0-{matchUsersCacheNum}）', 1
                return result
            loginUser = self.getLoginUser()
            if not loginUser:
                result['msg'], result['ret'] = '用户未登录', 1
                return result
            _id = loginUser['id']
            matchUserIdListCache = self.getMatchUserIdCache(_id)
            if not matchUserIdListCache:
                userIdCacheKey = f'match:user:{_id}'
                tags = loginUser['tags']
                userTuple = self.query().filter(
                    self.table.id != _id,
                    self.table.tags != "").with_entities(
                    self.table.id, self.table.tags)
                max_distance = 0
                """
                finish doto 待优化 不该查询所有记录 10w条记录遍历耗时22秒
                    主要在于对redis的操作 耗时 18-19秒左右
                    优化了 cur_num = redisClient.zcard(userIdCacheKey)，避免重复计算，现在整体耗时11s
                分析发现，主要是使用 zcard 的方法耗时长（9.5s左右），
                    于是维护了一个count变量来代替 zcard，优化后整体耗时1.25s，主要集中在算法上的耗时
                    这里并不是 zcard 本身耗时长，而是变量了10w次的累加
                """
                count = 0
                for user in userTuple:
                    userId = user.id
                    userTagList = json.loads(user.tags)
                    distance = algorithmUtils.minDistanceTag(tags, userTagList)
                    if count < matchUsersCacheNum:
                        redisClient.zadd(userIdCacheKey, {userId: distance})
                        max_distance = max(max_distance, distance)
                        count += 1
                    elif count >= matchUsersCacheNum and distance < max_distance:
                        popItem = redisClient.zrange(userIdCacheKey, matchUsersCacheNum-1, matchUsersCacheNum-1, withscores=True)
                        redisClient.zrem(userIdCacheKey, popItem[0][0])
                        redisClient.zadd(userIdCacheKey, {userId: distance})
                        max_distance = min(
                            max_distance,
                            redisClient.zrange(userIdCacheKey, matchUsersCacheNum-1, matchUsersCacheNum-1, withscores=True)[0][1])
                redisClient.expire(userIdCacheKey, 3600)
                matchUserIdListCache = self.getMatchUserIdCache(_id)
            # 按返回的idList来查询数据库
            matchUserQuery = self.table.query.filter(self.table.id.in_(matchUserIdListCache)).limit(num).all()
            for matchUser in matchUserQuery:
                result['data'].append(self.unifyItem(matchUser))
        except Exception as e:
            print(f'error happen: {e}', flush=True)
            result['msg'], result['ret'] = f'匹配失败：{e}', 1
        finally:
            return result

    def saveAvatar(self, file):
        result = {'msg': '成功', 'ret': 0}
        try:
            if not file.filename:
                result['msg'], result['ret'] = '未选择文件', 1
                return result
            loginUser = self.getLoginUser()
            if not loginUser:
                result['msg'], result['ret'] = '用户未登录', 1
                return result
            userId = loginUser['id']
            extend_name = file.filename.split('.')[-1]
            filename = f'userId_{userId}_avatar.{extend_name}'
            file.save(os.path.join('./static/avatars', secure_filename(filename)))
            dbSave = self.updateById({
                'id': userId,
                'avatarUrl': f'http://{HOST}:{PORT}/user/avatar/{filename}'})
            if not dbSave:
                result['msg'], result['ret'] = '更新失败', 1
                return result
        except Exception as e:
            print(f'error happen: {e}', flush=True)
            result['msg'], result['ret'] = f'更新失败：{e}', 1
        finally:
            return result

    def quitLogin(self, requestQuery):
        result = {'msg': '成功', 'ret': 0}
        try:
            userId = requestQuery.get('id', 0)
            loginUser = self.getLoginUser()
            if not userId:
                result['msg'], result['ret'] = '请求参数错误', 1
                return result
            if not loginUser or loginUser['id'] != userId:
                result['msg'], result['ret'] = '当前用户未登录', 1
                return result
            session.pop(USER_LOGIN_STATE, None)
        except Exception as e:
            print(f'error happen: {e}', flush=True)
            result['msg'], result['ret'] = f'操作失败：{e}', 1
        finally:
            return result

    def checkAccountExist(self, userAccount):
        query = self.query().filter_by(userAccount=userAccount).first()
        return True if query else False
