from service import teamService
from service.Base import base
from database import db, Team, User_Team, User
from utils import TeamStatusEnum
from datetime import datetime
from configs import JoinTeamLock


class userTeamService(teamService):
    def __init__(self):
        self.table = User_Team
        self.user_table = User
        self.team_table = Team
        self.base = base()

    def userQuery(self):
        return self.user_table.query.filter_by(isDelete=0)

    def teamQuery(self):
        return self.team_table.query.filter_by(isDelete=0)

    def count(self, userId, teamId=0):
        """
        计算 userId 一共加入和创建了多少个队伍
            或者是否尝试加入自己创建的队伍
        注意这里要过滤掉已过期的队伍
        """
        query = self.query().filter_by(userId=userId)
        if teamId > 0:
            query = query.filter_by(teamId=teamId)
        count = query.count()
        userIdQuery = query.with_entities(self.table.teamId)
        for item in userIdQuery:
            joinedTeamId = item.teamId
            teamExpireTimeQuery = self.team_table.query.filter_by(
                id=joinedTeamId, isDelete=0).first()
            if teamExpireTimeQuery and teamExpireTimeQuery.expireTime <= datetime.now():
                count -= 1
        return count

    def countUserNum(self, teamId):
        """
        计算加入teamId队伍的人数
        """
        return self.query().filter_by(teamId=teamId).count()

    def joinTeam(self, teamJoinRequest, loginUser):
        result = {'ret': 0, 'msg': 'success'}
        try:
            if not teamJoinRequest:
                result['msg'], result['ret'] = '参数设置为空', 1
                return result

            if not loginUser:
                result['msg'], result['ret'] = '当前用户未登录', 1
                return result

            teamId = teamJoinRequest.get('teamId', 0)
            if teamId <= 0:
                result['msg'], result['ret'] = '队伍ID不存在', 1
                return result

            self.base.setTable(Team)
            team = self.base.getById(teamId)
            if not team:
                result['msg'], result['ret'] = '队伍不存在', 1
                return result

            expireTime = team.expireTime
            if datetime.now() > expireTime:
                result['msg'], result['ret'] = '队伍已过期', 1
                return result

            status = team.status
            statusEnum = TeamStatusEnum.getEnumByValue(status)
            if statusEnum is None:
                statusEnum.value = TeamStatusEnum.PUBLIC.value
            elif (statusEnum.value == TeamStatusEnum.PRIVATE.value):
                result['msg'], result['ret'] = '不能加入私有队伍', 1
                return result

            password = teamJoinRequest.get('password', '')
            if statusEnum.value == TeamStatusEnum.SECRET.value:
                if not password or password != team.password:
                    result['msg'], result['ret'] = '队伍密码不正确', 1
                    return result
            LOCK = JoinTeamLock(teamId)
            if LOCK.acquire(blocking=True, timeout=5):
                userId = loginUser['id']
                hasJoinNum = self.count(userId)
                if hasJoinNum >= 5:
                    result['msg'], result['ret'] = '最多创建和加入5个队伍', 1
                    return result

                # todo 如果用户加入频繁，可能出现校验延迟
                hasUserJoinTeam = self.count(userId, teamId)
                if hasUserJoinTeam > 0:
                    result['msg'], result['ret'] = '用户已加入该队伍，不能重复加入已加入的队伍', 1
                    return result

                teamHasJoinNum = self.countUserNum(teamId)
                if teamHasJoinNum >= team.maxNum:
                    result['msg'], result['ret'] = '队伍已满，无法加入', 1
                    return result

                userTeam = self.table()
                userTeam.userId = userId
                userTeam.teamId = teamId

                save = self.save(userTeam)
                if not save:
                    result['msg'], result['ret'] = '修改队伍-用户关联信息失败', 1
                    return result
                
            else:
                print('加入队伍超时', flush=True)
                result['msg'], result['ret'] = '操作错误', 1
                return result
        except Exception as e:
            db.session.rollback()
            print(f'error happen: {e}')
            result['msg'], result['ret'] = '加入队伍失败', 1
        finally:
            if LOCK.locked():
                LOCK.release()
            return result

    def quitTeam(self, teamQuitRequest, loginUser):
        result = {'ret': 0, 'msg': 'success'}
        try:
            if not teamQuitRequest:
                result['msg'], result['ret'] = '参数设置为空', 1
                return result

            if not loginUser:
                result['msg'], result['ret'] = '当前用户未登录', 1
                return result

            teamId = teamQuitRequest.get('teamId', 0)
            if teamId <= 0:
                result['msg'], result['ret'] = '队伍ID不存在', 1
                return result

            self.base.setTable(Team)
            team = self.base.getById(teamId)
            if not team:
                result['msg'], result['ret'] = '队伍不存在', 1
                return result

            userId = loginUser['id']
            queryUserTeam = self.table()
            queryUserTeam.teamId = teamId
            queryUserTeam.userId = userId
            count = self.count(userId, teamId)
            if count == 0:
                result['msg'], result['ret'] = '未加入该队伍', 1
                return result
            teamHasJoinNum = self.countUserNum(teamId)
            if teamHasJoinNum == 1:
                self.base.removeById(teamId, need_commit=False)
            elif teamHasJoinNum > 1:
                if team.userId == userId:
                    userTeamList = self.list(teamId)
                    if len(userTeamList) <= 1:
                        result['msg'], result['ret'] = '队伍人数不足2人但没有被正常处理，请检查逻辑', 1
                        return result
                    nextUserTeam = userTeamList[1]
                    nextUserLeaderId = nextUserTeam.userId
                    team.userId = nextUserLeaderId

                    save = self.base.save(team)
                    if not save:
                        result['msg'], result['ret'] = '更新队伍队长失败', 1
                        return result
            else:
                result['msg'], result['ret'] = f'队伍加入的人数[{teamHasJoinNum}]不正确', 1
                return result
            self.remove(userId, teamId)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f'error happen: {e}')
            result['msg'], result['ret'] = '退出队伍失败', 1
        finally:
            return result

    def list(self, teamId, num=2):
        data = self.query().order_by('id').filter_by(
            teamId=teamId).limit(num).all()
        result = [_ for _ in data] if data else []
        return result

    def remove(self, userId, teamId):
        """
        将 用户-队伍 关系表中，用户（userId）加入的队伍（teamId）的 isDelete 改为1
        """
        item = self.query().filter_by(
            userId=userId,
            teamId=teamId).first()
        if item:
            item.isDelete = 1
            return True
        else:
            return False

    def deleteTeam(self, teamId, loginUser):
        result = {'ret': 0, 'msg': 'success'}
        try:
            if teamId <= 0:
                result['msg'], result['ret'] = '队伍ID不存在', 1
                return result

            if not loginUser:
                result['msg'], result['ret'] = '当前用户未登录', 1
                return result

            self.base.setTable(Team)
            team = self.base.getById(teamId)
            if not team:
                result['msg'], result['ret'] = '队伍不存在', 1
                return result

            if team.userId != loginUser['id']:
                result['msg'], result['ret'] = '非队长无权限解散队伍', 1
                return result

            removeAll = self.removeAllByTeamId(teamId)
            if not removeAll:
                result['msg'], result['ret'] = '删除 用户-队伍 关联表信息失败', 1
                return result
            self.base.removeById(teamId, need_commit=False)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f'error happen: {e}')
            result['msg'], result['ret'] = '退出队伍失败', 1
        finally:
            return result

    def removeAllByTeamId(self, teamId):
        data = self.query().filter_by(teamId=teamId).all()
        if not data:
            return False
        for item in data:
            item.isDelete = 1
        return True

    def getTeamIdListByUserId(self, userId):
        result = set()
        data = self.query().order_by(self.table.id).filter_by(
            userId=userId).with_entities(self.table.teamId)
        for item in data:
            result.add(item.teamId)
        return list(result)

    def setUserHasJoinTeam(self, teamList, loginUser):
        userId = loginUser.get('id', 0)
        userTeamList = self.getTeamIdListByUserId(userId)
        for team in teamList:
            if team['id'] in userTeamList:
                team['hasJoin'] = True

    def setUserInfo(self, teamList):
        for team in teamList:
            team['userInfo'] = []
            teamId = team['id']
            userIdTuple = self.query().filter_by(
                teamId=teamId).with_entities(
                self.table.userId)
            userIdList = []
            for userIdItem in userIdTuple:
                userIdList.append(userIdItem.userId)
            userQuery = self.userQuery().filter(
                User.id.in_(userIdList)).with_entities(User.avatarUrl)
            for item in userQuery:
                team['userInfo'].append({
                    'avatarUrl': item.avatarUrl
                    })
