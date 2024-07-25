from flask import Flask, make_response
from database import init_db
from flask_restx import Api, swagger
from flask_cors import CORS
from config import HOST_1
from controller import user_api, index_api, team_api
from redis_client import InitRedisDB
from configs import InitApscheduler
from job import StartJob


def create_app():
    app = Flask(__name__)
    init_db(app)
    InitRedisDB(app)
    InitApscheduler(app)
    CORS(app, origins=HOST_1, supports_credentials=True)

    api = Api(app,
        title='paopao API 文档',
        version='1.0版本',
        description='这是基于swagger的paopao-API 文档'
    )
    api.add_namespace(user_api)
    api.add_namespace(index_api)
    api.add_namespace(team_api)
    
    StartJob()  # 开启定时任务

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='localhost')
