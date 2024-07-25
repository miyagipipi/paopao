from flask import request
from flask_restx import Resource, Namespace, reqparse
from restxModels import TeamModel, TeamUserModel, TeamPlanModel
from service import (
    teamService, userService, userTeamService,
    teamPlanService)


api = Namespace('team', description='组队相关的 API')

team_service = teamService()
user_service = userService()
user_team_service = userTeamService()
team_plan_service = teamPlanService()

team_model = TeamModel(api)
team_user_model = TeamUserModel(api)
team_plan_model = TeamPlanModel(api)

@api.route('/add')
class teamAdd(Resource):
    @api.expect(team_model.add, validate=True)
    @api.marshal_with(team_model.add_result)
    def post(self):
        team = request.json
        if not team:
            api.abort(401, '接受的参数team为空')
        loginUser = user_service.getLoginUser()

        result = team_service.addTeam(
            team_service.dumpItem(team),
            loginUser)
        return result

@api.route('/list')
class teamList(Resource):
    @api.doc(params=team_model.get_list())
    @api.marshal_with(team_user_model.result_list)
    def get(self):
        teamQuery = request.args
        loginUser = user_service.getLoginUser()
        if not loginUser:
            result = {'msg': '用户未登录', 'ret': 1}
            return result
        isAdmin = user_service.isAdmin()
        result = team_service.listTeams(teamQuery, isAdmin)
        if result['ret'] == 1:
            return result
        user_team_service.setUserHasJoinTeam(
            result['data'],
            loginUser)
        user_team_service.setUserInfo(result['data'])
        return result

@api.route('/update')
class teamUpdate(Resource):
    @api.expect(team_model.update, validate=True)
    @api.marshal_with(team_model.result)
    def post(self):
        team = request.json
        if not team:
            api.abort(401, '更新失败，请求参数错误')
        loginUser = user_service.getLoginUser()
        result = team_service.updateTeam(team, loginUser)
        return result

@api.route('/join')
class teamJoin(Resource):
    @api.expect(team_model.join_expect, validate=True)
    @api.marshal_with(team_model.result)
    def post(self):
        teamJoinRequest = request.json
        if not teamJoinRequest:
            api.abort(401, '请求参数错误')
        loginUser = user_service.getLoginUser()
        result = user_team_service.joinTeam(teamJoinRequest, loginUser)
        return result

@api.route('/quit')
class teamQuit(Resource):
    @api.expect(team_model.quit_expect, validate=True)
    @api.marshal_with(team_model.result)
    def post(self):
        teamQuitRequest = request.json
        if not teamQuitRequest:
            api.abort(401, '请求参数错误')
        loginUser = user_service.getLoginUser()
        result = user_team_service.quitTeam(teamQuitRequest, loginUser)
        return result

@api.route('/delete')
class teamDelete(Resource):
    @api.expect(team_model.only_id, validate=True)
    @api.marshal_with(team_model.result)
    def post(self):
        data = request.json
        _id = data['id']
        if _id <= 0:
            api.abort(401, '队伍ID不存在')
        loginUser = user_service.getLoginUser()
        result = user_team_service.deleteTeam(_id, loginUser)
        return result

@api.route('/list/myCreate')
class teamListMyCreate(Resource):
    @api.doc(params=team_model.get_list())
    @api.marshal_with(team_user_model.result_list)
    def get(self):
        teamQuery = request.args.copy()
        loginUser = user_service.getLoginUser()
        if not loginUser:
            result = {'msg': '用户未登录', 'ret': 1}
            return result
        userId = loginUser.get('id', 0)
        teamQuery['userId'] = userId
        result = team_service.listTeams(teamQuery, True)
        if result['ret'] == 1:
            return result
        user_team_service.setUserHasJoinTeam(
            result['data'],
            loginUser)
        user_team_service.setUserInfo(result['data'])
        return result

@api.route('/list/myJoin')
class teamListMyJoin(Resource):
    @api.doc(params=team_model.get_list())
    @api.marshal_with(team_user_model.result_list)
    def get(self):
        teamQuery = request.args.copy()
        loginUser = user_service.getLoginUser()
        if not loginUser:
            result = {'msg': '用户未登录', 'ret': 1}
            return result
        userId = loginUser.get('id', 0)
        idList = team_service.filterMyJoinTeamIdList(
            user_team_service.getTeamIdListByUserId(userId),
            userId)
        
        if not idList:
            return {'msg': '', 'ret': 0}

        teamQuery['idList'] = idList
        result = team_service.listTeams(teamQuery, True)
        if result['ret'] == 1:
            return result
        user_team_service.setUserHasJoinTeam(
            result['data'],
            loginUser)
        user_team_service.setUserInfo(result['data'])
        return result


@api.route('/get')
class teamGetById(Resource):
    @api.doc(params=team_model.get_id_only())
    @api.marshal_with(team_model.result)
    def get(self):
        result = {}
        _id = int(request.args.get('id', type=str))
        if _id <= 0:
            api.abort(401, '查找失败，队伍ID小于1')
        team = team_service.getById(_id) # bool
        if not team:
            api.abort(401, '查找失败，队伍不存在')
        result['data'] = team
        return result


# todo 查询分页
@api.route('/list/page')
class teamListByPage(Resource):
    @api.doc(params=team_model.get_list_by_page())
    @api.marshal_with(team_model.result_list)
    def get(self):
        result = {}
        teamQuery = request.args
        if not teamQuery:
            api.abort(401, '查找失败，参数未正确设置')
        pageSize = int(teamQuery.get('pageSize', 0))
        pageNum = int(teamQuery.get('pageNum', 0))
        resultPage = team_service.page(pageSize, pageNum)
        result['data'] = resultPage
        return result

@api.route('/plan')
class teamPlan(Resource):
    @api.expect(team_plan_model.plan_request, validate=True)
    @api.marshal_with(team_plan_model.result_list)
    def post(self):
        queryData = request.json
        if not queryData or 'teamId' not in queryData:
            return {'msg': '参数错误', 'ret': 1}
        loginUser = user_service.getLoginUser()
        if not loginUser:
            return {'msg': '用户未登录', 'ret': 1}
        result = team_plan_service.getListByTeamId(
            int(queryData['teamId']),
            loginUser['id'])
        return result

@api.route('/plan/add')
class teanPlanAdd(Resource):
    @api.expect(team_plan_model.add_request, validate=True)
    @api.marshal_with(team_plan_model.result_list)
    def post(self):
        result = {'msg': '操作成功', 'ret': 0}
        queryData = request.json.copy()
        if not queryData or 'teamId' not in queryData:
            return {'msg': '参数错误', 'ret': 1}
        loginUser = user_service.getLoginUser()
        if not loginUser:
            return {'msg': '用户未登录', 'ret': 1}
        queryData['userId'] = loginUser['id']
        save = team_plan_service.save(queryData)
        if not save:
            return {'msg': '操作失败', 'ret': 1}
        return result
