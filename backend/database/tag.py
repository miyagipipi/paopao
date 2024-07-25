from database.base import db
from datetime import datetime


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    tagName = db.Column(db.String(255))
    userId = db.Column(db.BigInteger)
    parentId = db.Column(db.BigInteger)
    isParent = db.Column(db.Integer)
    createTime = db.Column(db.DateTime)
    updateTime = db.Column(db.DateTime, default=datetime.now())
    isDelete = db.Column(db.Integer)
    
    def __repr__(self):
        return '<tag %r>' % self.username