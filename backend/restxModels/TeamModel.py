from flask_restx import fields


class TeamModel(object):
    """docstring for IndexModel"""
    def __init__(self, api):
        self.api = api

        # 组队的模型
        self.team = api.model('team model', {
            'id': fields.Integer(required=True, description='team ID in database'),
            'name': fields.String(required=True, description='team name'),
            'description': fields.String(description='team description'),
            'maxNum': fields.Integer(description='team max member number', default=1),
            'expireTime': fields.DateTime(description='expire time'),
            'userId': fields.Integer(description='user id'),
            'status': fields.Integer(description='team status', default=0),
            'password': fields.String(description='password', default='123456'),
            'createTime': fields.DateTime(description='createTime'),
            'updateTime': fields.DateTime(description='updateTime'),
            'isDelete': fields.Integer(description='is delete', default=0)
        })

        # 增加队伍的模型
        self.add = api.model('add team', {
            'name': fields.String(required=True, description='team name'),
            'description': fields.String(description='team description'),
            'maxNum': fields.Integer(description='team max member number', default=2),
            'expireTime': fields.DateTime(description='expire time'),
            'userId': fields.Integer(description='user id'),
            'status': fields.Integer(description='team status', default=0),
            'password': fields.String(description='password', default='123456')
        })
        self.add_result = api.model('add team response', {
            'msg': fields.String(
                required=True,
                default='success',
                description='Message of the response',
                attribute='msg'),
            'ret': fields.Integer(
                required=True,
                default=0,
                description='Return code of the response'),
            'teamId': fields.Integer(required=True, description='added team id', default=-1)
            })

        # 只使用了ID的模型
        self.only_id = api.model('used for request only need id', {
            'id': fields.Integer(required=True, description='team ID in database')
        })

        # 组队的模型
        self.update = api.model('update team', {
            'id': fields.Integer(required=True, description='team ID in database'),
            'name': fields.String(description='team name'),
            'description': fields.String(description='team description'),
            # 'maxNum': fields.Integer(description='team max member number', default=1),
            'expireTime': fields.DateTime(description='expire time'),
            'status': fields.Integer(description='team status', default=0),
            'password': fields.String(description='password', default='123456')
        })

        self.result = api.model('team query result', {
            'msg': fields.String(
                required=True,
                default='success',
                description='Message of the response',
                attribute='msg'),
            'ret': fields.Integer(
                required=True,
                default=0,
                description='Return code of the response'),
            'data': fields.Nested(self.team, default={}, description='return data')
        })

        self.result_list = api.model('team list query result', {
            'msg': fields.String(
                required=True,
                default='success',
                description='Message of the response',
                attribute='msg'), # 重命名属性 + 默认值
            'ret': fields.Integer(required=True, description='Return code of the response', default=0),
            'data': fields.List(fields.Nested(self.team), description='List of users matching the tags')
        })

        self.join_expect = api.model('join team request', {
            'teamId': fields.Integer(
                required=True,
                description='要加入的队伍ID'),
            'password': fields.String(
                description='队伍密码'
            )
        })

        self.quit_expect = api.model('quit team request', {
            'teamId': fields.Integer(
                required=True,
                description='要退出的队伍ID')
        })

    def get_id_only(self):
        return {
            'id': {
                'description': '队伍ID',
                'required': True
            }
        }

    def get_list(self):
        parse = {
            'id': {'description': '队伍ID', 'type': 'int'},
            'idList': {'description': '队伍ID列表', 'type': 'list'},
            'searchText': {'description': '全文搜索'},
            'name': {},
            'description': {},
            'maxNum': {'type': 'int'},
            'userId': {'type': 'int'},
            'status': {'type': 'int'},
            'searchText': {'type': 'string'}
        }
        return parse

    def get_list_by_page(self):
        parse = self.get_list()
        parse['pageNum'] = {
            'description': '第几页',
            'type': 'int'
        }
        parse['pageSize'] = {
            'description': '一页的数量',
            'type': 'int'
        }
        return parse
