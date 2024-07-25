from service.Base import base
from service import teamService
from database import db, Team_Plan, Team, User_Team
from utils import unionTeamPlanItem


class teamPlanService(teamService):
    def __init__(self):
        self.table = Team_Plan
        self.team_table = Team
        self.user_team_table = User_Team
        self.base = base()

    def unifyItem(self, item):
        """
        Team ORM transilate to dict
        """
        return unionTeamPlanItem(item)

    def getListByTeamId(self, teamId, userId):
        result = {'msg': '请求成功', 'ret': 0, 'data': []}
        try:
            # 队伍是否存在
            self.base.setTable(Team)
            if not self.base.getById(teamId):
                result['msg'], result['ret'] = '队伍不存在', 1
                return result
            # 用户是否加入队伍
            if not self.user_team_table.query.filter_by(
                teamId=teamId, userId=userId, isDelete=0).first():
                result['msg'], result['ret'] = '用户未加入当前队伍', 1
                return result
            plans = self.query().filter_by(teamId=teamId).order_by(self.table.id).all()
            for plan in plans:
                planVO = self.unifyItem(plan)
                result['data'].append(planVO)
        except Exception as e:
            print(f'error happen: {e}')
            result['msg'], result['ret'] = '请求失败', 1
        finally:
            return result
