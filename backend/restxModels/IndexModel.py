from flask_restx import fields


class IndexModel(object):
    """docstring for IndexModel"""
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
            'profile': fields.String(description='profile'),
            # 'userRole': fields.Integer(description='userRole'),
            'createTime': fields.String(description='createTime'),
        })

        # 主页中的推荐用户的响应模型
        self.index_recommend_user_model = api.model('主页中的推荐用户的响应模型', {
            'msg': fields.String(
                required=True,
                default='success',
                description='Message of the response',
                attribute='msg'), # 重命名属性 + 默认值
            'ret': fields.Integer(required=True, description='Return code of the response'),
            'data': fields.List(fields.Nested(self.user_model), description='recommend users')
        })

        # self.result_model = api.model('unionResultModel', {
        #     'msg': fields.String(
        #         required=True,
        #         default='success',
        #         description='Message of the response',
        #         attribute='msg'),
        #     'ret': fields.Integer(required=True, description='Return code of the response'),
        #     'data': fields.Nested(self.user_model, default={}, description='return data')
        # })
