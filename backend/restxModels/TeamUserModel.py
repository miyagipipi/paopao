from flask_restx import fields


class TeamUserModel(object):
    """docstring for UserModel"""
    def __init__(self, api):
        self.api = api

        self.createUser = api.model('创建人用户模型', {
                'id': fields.Integer(required=True, description='user ID in database'),
                'username': fields.String(required=True, description='The user name'),
                'userAccount': fields.String(description='userAccount'),
                'avatarUrl': fields.String(description='avatarUrl'),
                'gender': fields.Integer(description='gender'),
                'phone': fields.String(description='phone'),
                'email': fields.String(description='email'),
                'userStatus': fields.Integer(description='userStatus'),
                'createTime': fields.String(description='createTime'),
                'updateTime': fields.String(description='updateTime'),
                'planetCode': fields.String(description='planetCode'),
                'tags': fields.String(description='The user tags'),
                'profile': fields.String(description='profile'),
                'userRole': fields.Integer(description='userRole')
            })

        self.user_info = api.model('加入队伍的用户信息', {
                'avatarUrl': fields.String(description='user avatar url')
            })

        # 展示在组队前端页面的模型
        self.team_list = api.model('队伍和用户信息模型', {
            'id': fields.Integer(required=True, description='team ID in database'),
            'name': fields.String(required=True, description='team name'),
            'description': fields.String(description='team description'),
            'maxNum': fields.Integer(description='team max member number', default=2),
            'expireTime': fields.DateTime(description='expire time'),
            'userId': fields.Integer(description='user id'),
            'status': fields.Integer(description='team status', default=0),
            'createTime': fields.DateTime(description='createTime'),
            'updateTime': fields.DateTime(description='updateTime'),
            'createUser': fields.Nested(self.createUser, required=True),
            'hasJoin': fields.Boolean(description='has join current team', default=False),
            'userInfo': fields.List(fields.Nested(self.user_info), description='joined user info', default=[])
        })

        self.result_list = api.model('/team/list 查询接口的响应模型', {
            'msg': fields.String(
                required=True,
                default='success',
                description='Message of the response',
                attribute='msg'), # 重命名属性 + 默认值
            'ret': fields.Integer(required=True, description='Return code of the response', default=0),
            'data': fields.List(fields.Nested(self.team_list), description='List of team', default=[])
        })
