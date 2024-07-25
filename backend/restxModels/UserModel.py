from flask_restx import fields


class UserModel(object):
    """docstring for UserModel"""
    def __init__(self, api):
        self.api = api

        # 定义用户对象的模型
        self.user_model = api.model('UserDetail', {
            'id': fields.Integer(required=True, description='user ID in database'),
            'username': fields.String(required=True, description='The user name'),
            'userAccount': fields.String(description='userAccount'),
            'avatarUrl': fields.String(description='avatarUrl'),
            'gender': fields.Integer(description='gender'),
            'phone': fields.String(description='phone'),
            'email': fields.String(description='email'),
            'planetCode': fields.String(description='planetCode'),
            'tags': fields.List(fields.String, description='The user tags'),
            'profile': fields.String(description='profile', default='这个人很懒，没有任何介绍'),
            # 'userRole': fields.Integer(description='userRole'),
            'createTime': fields.String(description='createTime'),
        })

        # 定义搜索用户的响应模型
        self.result_list = api.model('SearchUsersResponse', {
            'msg': fields.String(
                required=True,
                default='success',
                description='Message of the response',
                attribute='msg'), # 重命名属性 + 默认值
            'ret': fields.Integer(required=True, description='Return code of the response'),
            'data': fields.List(
                fields.Nested(self.user_model),
                default=[],
                description='List of users matching the tags')
        })
        self.tag_names_model = api.model('TagNamesModel', {
            'data': fields.List(fields.String, required=True, description='标签名称列表')
        })
        self.user_login_model = api.model('userLoginModel', {
            'userAccount': fields.String(
                required=True,
                description='user account'),
            'userPassword': fields.String(
                required=True,
                description='user password')
        })
        self.result_model = api.model('unionResultModel', {
            'msg': fields.String(
                required=True,
                default='success',
                description='Message of the response',
                attribute='msg'),
            'ret': fields.Integer(required=True, description='Return code of the response'),
            'data': fields.Nested(self.user_model, default={}, description='return data')
        })
        self.check_login = api.model('check user login status', {
            'msg': fields.String(
                required=True,
                default='success',
                description='Message of the response',
                attribute='msg'),
            'ret': fields.Integer(required=True, description='Return code of the response'),
            'id': fields.Integer(description='user id', default=0)
            })

        self.account_exist_request = api.model('account_exist_request', {
            'userAccount': fields.String(required=True)
            })

        self.register_request = api.model('register_request', {
            'username': fields.String(required=True),
            'userAccount': fields.String(required=True),
            'gender': fields.Integer(required=True),
            'userPassword': fields.String(required=True),
            'phone': fields.String(),
            'email': fields.String(),
            'tags': fields.List(fields.String, description='The user tags'),
            })

    def get_match(self):
        parse = {
            'num': {'description': '匹配用户数量', 'type': 'int'}
        }
        return parse
