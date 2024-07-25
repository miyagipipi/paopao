"""
move it to ./controller to insert users
"""

from flask_restx import Resource, Namespace
from database import db_session, User
import random, time, json
from datetime import datetime
from threading import Thread


api = Namespace('addUsers', description='批量导入用户 API')


@api.route('/toUserDB')
class addUsersToUserDB(Resource):
    """
    批量导入1000w条用户数据到数据库
        1000条 = 2秒
        10w条 =  88秒
    并发导入10w条，分成10组，每组1w条
    """
    def get(self):
        start = int(time.time())

        result = {'msg': '成功', 'ret': 0, 'count': 0}
        insert_num = 100000
        threads = []
        for i in range(10):
            thread = Thread(target=lambda: self.insert_users())
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()

        print(f'插入{insert_num}一共用时: {int(time.time()) - start}')
        return result

    def insert_users(self):
        session = db_session()
        try:
            for j in range(10000):
                new_user = User(
                    username = '假用户',
                    userAccount = 'faketianxiao',
                    avatarUrl = 'https://i1.hdslb.com/bfs/face/4d9393f71443ec1168dc50cc5ebb2a73325b53f9.jpg',
                    gender = random.randint(1,2),
                    userPassword = '123456',
                    phone = str(random.randint(10000000000, 15799999999)),
                    email = 'fakeEmail@gmail.com',
                    userStatus = 0,
                    createTime = datetime.now(),
                    planetCode = str(random.randint(10000000, 30000000)),
                    tags = json.dumps(["python"]),
                    profile = 'im bot',
                )
                session.add(new_user)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f'数据库操作出错： {e}')
        return
