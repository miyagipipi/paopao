from database.base import db
from datetime import datetime


class User_Team(db.Model):
    __tablename__ = 'user_team'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer)
    teamId = db.Column(db.Integer)
    joinTime = db.Column(db.DateTime, default=datetime.now())
    createTime = db.Column(db.DateTime, default=datetime.now())
    updateTime = db.Column(db.DateTime, default=datetime.now())
    isDelete = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<User_Team %r>' % self.name