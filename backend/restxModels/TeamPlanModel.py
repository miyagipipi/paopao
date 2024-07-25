from flask_restx import fields


class TeamPlanModel(object):
    """docstring for TeamPlanModel"""
    def __init__(self, api):
        self.api = api

        # 定义用户对象的模型
        self.team_plan_model = api.model('TeamPlanModel', {
            'id': fields.Integer(required=True, description='team_plan ID in database'),
            'title': fields.String(description='title'),
            'description': fields.String(description='description'),
            'createTime': fields.DateTime(description='createTime')
        })

        # 定义搜索用户的响应模型
        self.result_list = api.model('Response', {
            'msg': fields.String(
                required=True,
                default='success',
                description='Message of the response',
                attribute='msg'),
            'ret': fields.Integer(required=True, description='Return code of the response'),
            'data': fields.List(
                fields.Nested(self.team_plan_model),
                default=[],
                description='List of team plan')
        })

        self.plan_request = api.model('plan_request', {
            'teamId': fields.Integer(required=True, description='teamId'),
        })

        self.add_request = api.model('add_request', {
            'teamId': fields.Integer(required=True, description='teamId'),
            'title': fields.String(required=True, description='title'),
            'description': fields.String(required=True, description='description'),
        })

