from database.base import db
from datetime import datetime


class Team_Plan(db.Model):
    __tablename__ = 'team_plan'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer)
    teamId = db.Column(db.Integer)
    title = db.Column(db.String)
    description = db.Column(db.String)
    createTime = db.Column(db.DateTime, default=datetime.now())
    updateTime = db.Column(db.DateTime, default=datetime.now())
    isDelete = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Team_Plan %r>' % self.name