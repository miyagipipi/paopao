# user_routes.py
from flask import session, request, send_from_directory
from database import User
from sqlalchemy import and_
from flask_restx import Resource, Namespace
from config import USER_LOGIN_STATE
from common import *
from service import userService, adminService
from restxModels import UserModel


api = Namespace('user', description='通过标签查询用户 API')
model = UserModel(api)
user_service = userService()


@api.route('/searchUsersByTags')
class userSearchUsersByTags(Resource):
    @api.expect(model.tag_names_model)  # 使用 expect 来指定输入模型
    @api.marshal_with(model.result_list)
    def post(self):
        tagNameList = api.payload['data']
        result = {'msg': '成功', 'ret': 0, 'data': []}
        conditions = [User.tags.like('%{}%'.format(tagName)) for tagName in tagNameList]
        users = User.query.filter(and_(*conditions)).all()
        for user in users:
            item = user_service.unifyItem(user)
            result['data'].append(item)

        return result

@api.route('/update')
class userUpdate(Resource):
    """
    1. 校验参数是否为空 2. 校验权限 3. 触发更新
    """
    def post(self):
        result = {'msg': '成功', 'ret': 0}
        update_data = api.payload

        if not update_data or not update_data['id']:
            return api.abort(401, '更新失败')
        loginUser = user_service.getLoginUser(session)
        if not loginUser:
            api.abort(401, '获取用户信息失败，请刷新页面重新登录')

        update_result = user_service.updateUser(update_data, loginUser)
        result['data'] = {'update_result': update_result}

        return result

@api.route('/adminLogin')
class userAdminLogin(Resource):
    @api.expect(model.tag_names_model)
    @api.marshal_with(model.result_model)
    def post(self):
        result = {'msg': '成功', 'ret': 0}
        data = api.payload['data']
        admin_service = adminService()
        admin = admin_service.getAdminUser()

        if admin:
            item = user_service.unifyItem(admin)
            result['data'] = item
        else:
            api.abort(401, '遇到问题...')
        return result

@api.route('/login')
class userLogin(Resource):
    @api.expect(model.user_login_model)
    @api.marshal_with(model.result_model)
    def post(self):
        result = {'msg': '成功', 'ret': 0}
        payload = api.payload
        userAccount, userPassword = payload['userAccount'], payload['userPassword']
        user = User.query.filter_by(userAccount=userAccount, userPassword=userPassword).first()
        if user:
            session.pop(USER_LOGIN_STATE, None)
            item = user_service.unifyItem(user)
            result['data'] = item
            session[USER_LOGIN_STATE] = item  # 设置session值
        else:
            api.abort(401, '登录失败')
        return result

@api.route('/current')
class userCurrent(Resource):
    @api.marshal_with(model.result_model)
    def get(self):
        result = {'msg': '成功', 'ret': 0}
        data = session.get(USER_LOGIN_STATE, None)
        if data:
            result['data'] = data
            result['msg'] = '获取用户信息成功'
        else:
            result['msg'], result['ret'] = '未登录或会话已过期', 1
        return result

@api.route('/match')
class userMatch(Resource):
    @api.doc(params=model.get_match())
    @api.marshal_with(model.result_list)
    def get(self):
        teamQuery = request.args.copy()
        result = {'msg': '成功', 'ret': 0, 'data': []}
        num = int(teamQuery.get('num', 0))
        result = user_service.matchUsers(num)
        return result

@api.route('/upload/avatar')
class userUploadAvatar(Resource):
    def post(self):
        file = request.files['avatar']
        result = user_service.saveAvatar(file)
        return result

@api.route('/avatar/<filename>')
class userAvatarUrl(Resource):
    def get(self, filename):
        return send_from_directory('./static/avatars/', filename)

@api.route('/checkLogin')
class userCheckLogin(Resource):
    @api.marshal_with(model.check_login)
    def get(self):
        result = {'msg': '成功', 'ret': 0}
        data = session.get(USER_LOGIN_STATE, None)
        if data:
            result['id'] = data['id']
            result['msg'] = '获取用户信息成功'
        else:
            result['msg'], result['ret'] = '未登录或会话已过期', 1
        return result

@api.route('/quit')
class userQuit(Resource):
    def post(self):
        result = user_service.quitLogin(request.json)
        return result

@api.route('/account/exist')
class userAccountExist(Resource):
    @api.expect(model.account_exist_request, validate=True)
    @api.marshal_with(model.result_model)
    def post(self):
        result = {'msg': '成功', 'ret': 0}
        queryData = request.json
        exist = user_service.checkAccountExist(queryData['userAccount'])
        if exist:
            result['msg'], result['ret'] = '用户已存在', 1
        return result

@api.route('/register')
class userRegister(Resource):
    @api.expect(model.register_request, validate=True)
    @api.marshal_with(model.result_model)
    def post(self):
        queryData = request.json
        save = user_service.save(queryData)
        if not save:
            return {'msg': '操作失败', 'ret': 1}
        return {'msg': '成功', 'ret': 0}

@api.route('/totalTags')
class userTotalTags(Resource):
    def get(self):
        return {'msg': '成功', 'ret': 0, 'data': user_service.getTotalTags()}
