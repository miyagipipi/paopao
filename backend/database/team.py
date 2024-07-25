from database.base import db
from datetime import datetime


class Team(db.Model):
    __tablename__ = 'team'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(1024))
    maxNum = db.Column(db.Integer, default=1)
    expireTime = db.Column(db.DateTime)
    userId = db.Column(db.Integer)
    status = db.Column(db.Integer, default=0)
    password = db.Column(db.String(512))
    createTime = db.Column(db.DateTime, default=datetime.now())
    updateTime = db.Column(db.DateTime, default=datetime.now())
    isDelete = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Team %r>' % self.name