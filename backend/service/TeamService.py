from .Base import base
from database import db, Team, User_Team, User
from utils import unionTeamItem, TeamStatusEnum, unionUserItem
from datetime import datetime
from common import FromatStrToDateTime
from sqlalchemy import or_, and_
from config import ADMIN_ROLE


base_service = base()


class teamService(base):
    def __init__(self):
        self.table = Team

    def unifyItem(self, item):
        """
        Team ORM transilate to dict
        """
        return unionTeamItem(item)

    def dumpItem(self, item):
        if 'expireTime' in item and item['expireTime'] != '':
            item['expireTime'] = FromatStrToDateTime(item['expireTime'])
        return super().dumpItem(item)

    def addTeam(self, team, loginUser):
        # 用户可以创建一个队伍，设置队伍的人物、名称、描述、超时时间、是否公开等等（P0）
        # 1. 请求参数是否为空，是否正确
        result = {'msg': '', 'ret': 0}
        try:
            if not team:
                result['msg'], result['ret'] = '请求参数team错误', 1
                return result

            # 2. 是否登录，未登录不允许创建
            if not loginUser:
                result['msg'], result['ret'] = '当前用户未登录', 1
                return result

            userId = loginUser['id']

            # 3. 校验信息：
            #     1. 队伍人物 > 1 且 <= 20
            maxNum = team.maxNum # 为空则返回0
            if maxNum <= 1 or maxNum > 20:
                result['msg'], result['ret'] = '队伍人数不满足要求（人数：2-20）', 1
                return result

            # 2. 队伍标题长度 <= 20
            name = team.name
            if not name.strip() or len(name) > 20:
                result['msg'], result['ret'] = '队伍标题长度不符合要求（1-20）', 1
                return result

            # 3. 描述长度 <= 512
            description = team.description
            if not description.strip() or len(description) > 512:
                result['msg'], result['ret'] = '队伍描述长度不符合要求（1-512）', 1
                return result

            # 4. status 是否公开（int），不传则默认为0-公开
            status = team.status
            statusEnum = TeamStatusEnum.getEnumByValue(status)
            if statusEnum is None:
                result['msg'], result['ret'] = '队伍状态不符合要求', 1
                return result

            # 5. 如果 status 是加密状态且密码存在的话，密码长度 <= 32
            password = team.password
            if TeamStatusEnum.SECRET.value == statusEnum.value:
                if password == '' or len(password) > 32:
                    result['msg'], result['ret'] = '密码设置不正确（最多32位）', 1
                    return result

            # 6. 超时时间 > 当前时间
            expireTime = team.expireTime
            if datetime.now() > expireTime:
                result['msg'], result['ret'] = '过期时间大于当前时间', 1
                return result

            # 7. 校验用户最多创建5个队伍 单表查询
            hasTeamNum = self.table.query.filter_by(userId=userId, isDelete=0).count()
            if hasTeamNum >= 5:
                result['msg'], result['ret'] = '用户最多创建 5 个队伍', 1
                return result

            # 8. 插入队伍信息到队伍表
            team.userId = userId

            db.session.add(team)
            db.session.flush()

            teamId = team.id
            if not teamId:
                result['msg'], result['ret'] = '创建队伍失败，没有teamID', 1
                return result

            # 9. 插入用户 => 队伍关系到关系表 注意要和8需要看做一个事务，保证原子性
            userTeam = User_Team()
            userTeam.userId = userId
            userTeam.teamId = teamId
            userTeam.joinTime = datetime.now()

            db.session.add(userTeam)
            db.session.flush()

            if not userTeam.id:
                result['msg'], result['ret'] = '创建队伍失败，没有userTeamID', 1
                return result

            result['teamId'] = teamId
            db.session.commit()
            return result
        except Exception as e:
            print(f'error happen: {e}')
            db.session.rollback()
            result['msg'], result['ret'] = '创建队伍失败', 1
            return result

    def listTeams(self, teamQuery, isAdmin):
        result = {'msg': '', 'ret': 0, 'data': []}
        query = self.table.query.filter_by(isDelete=0)
        try:
            # 1. 组合查询条件
            if teamQuery:
                _id = int(teamQuery.get('id', 0))
                if _id > 0:
                    query = query.filter_by(id=_id)

                idList = teamQuery.get('idList', [])
                if len(idList) > 0:
                    query = query.filter(self.table.id.in_(idList))

                # searchText 如果存在则对 name 和 descirption 同时搜索
                searchText = teamQuery.get('searchText', '')
                if searchText:
                    conditions = [
                        self.table.name.like('%{}%'.format(searchText)),
                        self.table.description.like('%{}%'.format(searchText))
                    ]
                    query = query.filter(or_(*conditions))
                
                name = teamQuery.get('name', '')
                if name:
                    query = query.filter(self.table.name.like('%{}%'.format(name)))

                description = teamQuery.get('description', '')
                if description:
                    query = query.filter(self.table.description.like('%{}%'.format(description)))

                # 查询最大 人数相等的
                maxNum = int(teamQuery.get('maxNum', 0))
                if maxNum > 0:
                    query = query.filter_by(maxNum=maxNum)

                # 根据创建人来查询
                userId = int(teamQuery.get('userId', 0))
                if userId > 0:
                    query = query.filter_by(userId=userId)

                # 根据状态来查询
                status = int(teamQuery.get('status', -1))
                statusEnum = TeamStatusEnum.getEnumByValue(status)
                if statusEnum:
                    query = query.filter(self.table.status == statusEnum.value)

            # 不展示已过期的队伍
            query = query.filter(self.table.expireTime > datetime.now())
            teamList = query.all()
            if not teamList:
                result['msg'] = '未查询到任何队伍'
                return result

            base_service.setTable(User)
            teamUserVOList = []
            for team in teamList:
                userId = team.userId
                if not userId:
                    continue
                user = base_service.getById(userId)
                teamUserVO = self.unifyItem(team)
                if user:
                    userVO = base_service.unifyItem(user, unionUserItem)
                    teamUserVO['createUser'] = userVO
                teamUserVOList.append(teamUserVO)
            result['data'] = teamUserVOList
            return result
        except Exception as e:
            print(f'error happen: {e}')
            result['msg'], result['ret'] = '查找失败', 1
            return result

    def updateTeam(self, team, loginUser):
        result = {'ret': 0, 'msg': 'success'}
        try:
            if not team:
                result['msg'], result['ret'] = '参数设置为空', 1
                return result
            if not loginUser:
                result['msg'], result['ret'] = '当前用户未登录', 1
                return result
            _id = int(team.get('id', 0))
            if _id <= 0:
                result['msg'], result['ret'] = '队伍ID不存在', 1
                return result
            oldTeam = self.getById(_id)
            if not oldTeam:
                result['msg'], result['ret'] = '原始队伍不存在', 1
                return result
            if (oldTeam.userId != loginUser['id'] and loginUser['userRole'] != ADMIN_ROLE):
                result['msg'], result['ret'] = '无权修改当前队伍', 1
                return result

            status = team.get('status', -1)
            statusEnum = TeamStatusEnum.getEnumByValue(status)
            if statusEnum is None:
                statusEnum.value = TeamStatusEnum.PUBLIC.value
            elif (statusEnum.value != TeamStatusEnum.PUBLIC.value
                and statusEnum.value != oldTeam.status
                and not team.get('password', '')):
                result['msg'], result['ret'] = '非公开的队伍需要设置密码', 1
                return result

            updateResult = self.updateById(team)
            if not updateResult:
                result['msg'], result['ret'] = '更新队伍信息失败', 1
                return result
        except Exception as e:
            print(f'error happen: {e}')
            result['msg'], result['ret'] = '更新队伍失败', 1
        finally:
            return result

    def filterMyJoinTeamIdList(self, idList, userId):
        result = []
        teamQuery = self.query().filter(
            self.table.id.in_(idList)).with_entities(
            self.table.id, self.table.userId)
        for item in teamQuery:
            if item.userId != userId:
                result.append(item.id)
        return result
