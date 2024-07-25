from flask_restx import Resource, Namespace, reqparse
from restxModels import UserModel, IndexModel
from service import userService
from redis_client import createRedisClient
import json


api = Namespace('index', description='首页相关的 API')
model = IndexModel(api)
user_service = userService()
parser = reqparse.RequestParser()
parser.add_argument('pageSize', type=int, required=True, help='一页的user数量', location='args')
parser.add_argument('pageNum', type=int, required=True, help='第几页', location='args')

redisClient = createRedisClient()


@api.route('/recommend')
class indexRecommend(Resource):
    @api.expect(parser)
    @api.marshal_with(model.index_recommend_user_model)
    def get(self):
        """
        接受两个参数： pageSize 和 pageNum
        pageSize = 一页的user数量
        pageNum = 第几页
        前端使用了无线滚动技术，后端不再缓存数据
        """
        result = {'msg': '成功', 'ret': 0, 'data': []}
        args = parser.parse_args()
        pageSize = args['pageSize']
        pageNum = args['pageNum']

        userPage = user_service.page(pageSize, pageNum)
        result['data'] = userPage
        return result
