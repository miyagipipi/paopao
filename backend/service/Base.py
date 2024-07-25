from database import db
from flask import session
from config import USER_LOGIN_STATE, ADMIN_ROLE, TAG_PATH
import json


class base(object):
    """
    docstring for base
    base class about database operations should not to commit,
    let other service class to commit, ensure the atomicity of transactions.
    """
    def __init__(self):
        self.table = None
    
    def setTable(self, table):
        self.table = table

    def query(self):
        return self.table.query.filter_by(isDelete=0) if self.table else None

    def unifyItem(self, item, fn):
        """
        Team ORM transilate to dict
        """
        return fn(item)

    def getLoginUser(self, session=session):
        """
        获取当前用户的登录信息
        """
        return session.get(USER_LOGIN_STATE, None)

    def isAdmin(self):
        """
        是否为管理员
        """
        user = self.getLoginUser()
        if user and user['userRole'] == ADMIN_ROLE:
            return True
        else:
            return False

    def OverrideIsAdmin(self, loginUser):
        """
        当前用户登录信息存在且为管理员
        """
        return loginUser != None and loginUser.get('userRole', -1) == ADMIN_ROLE

    def dumpItem(self, item):
        """
        dump dict to ORM and not commit
        """
        if not self.table:
            return None
        try:
            new_item = self.table()
            for k, v in item.items():
                if k != 'id' and hasattr(new_item, k):
                    setattr(new_item, k, v)
            return new_item
        except Exception as e:
            print(f'dump to ORM error: {e}', flush=True)
            return None

    def save(self, item, need_commit=True):
        """
        dict save to ORM
        """
        if not self.table:
            return False
        try:
            new_item = self.dumpItem(item) if isinstance(item, dict) else item
            if not new_item:
                print(f'save to ORM error: {e}', flush=True)
                return False
            db.session.add(new_item)
            if need_commit:
                db.session.commit()
            return True
        except Exception as e:
            if need_commit:
                db.session.rollback()
            print(f'save to ORM error: {e}', flush=True)
            return False

    def removeById(self, _id, need_commit=True):
        result = False
        if not self.table:
            return result
        try:
            data = self.table.query.filter_by(id=_id).first()
            if data:
                data.isDelete = 1
                result = True
                if need_commit:
                    db.session.commit()
            return result
        except Exception as e:
            if need_commit:
                db.session.rollback()
            print(f'delete error: {e}', flush=True)
            return False

    def updateById(self, item, need_commit=True):
        if not self.table:
            return False
        try:
            _id = item.get('id', 0)
            if _id == 0:
                return False
            self.table.query.filter_by(id=_id).update(item)
            if need_commit:
                db.session.commit()
            return True
        except Exception as e:
            if need_commit:
                db.session.rollback()
            print(f'delete error: {e}', flush=True)
            return False

    def getById(self, _id):
        if not self.table:
            return False
        try:
            data = self.table.query.filter_by(id=_id).first()
            return data
        except Exception as e:
            print(f'getById[{_id}] error: {e}', flush=True)
            return False

    def getList(self, item):
        array = []
        if not self.table:
            return array
        try:
            query = self.table.query.filter_by(isDelete=0)
            for k, v in item.items():
                query = query.filter(getattr(self.table, k) == v)
            tables = query.all()
            for table in tables:
                new_item = self.unifyItem(table) # unfiyItem 对应各自子类的格式化方法
                array.append(new_item)
            return array
        except Exception as e:
            print(f'getList error: {e}', flush=True)
            return []

    def page(self, pageSize, pageNum):
        """
        pageSize: 一页的数量 default=10
        pageNum: 第几页 default=1
        """
        pageSize = 10 if not pageSize else pageSize
        pageNum = 1 if not pageNum else pageNum
        array = []
        if not self.table:
            return array
        try:
            offset = (pageNum - 1) * pageSize
            tables = self.table.query.order_by(
                self.table.id).filter_by(
                isDelete=0).limit(pageSize).offset(offset).all()
            for table in tables:
                new_item = self.unifyItem(table)
                array.append(new_item)
            return array
        except Exception as e:
            print(f'get list by page error: {e}', flush=True)
            return []

    def getTotalTags(self):
        data = []
        with open(TAG_PATH, encoding='utf-8') as f:
            raw_data = json.load(f)
            for raw_item in raw_data:
                for child in raw_item['children']:
                    child['id'] = child['text']
                data.append(raw_item)
        return data
