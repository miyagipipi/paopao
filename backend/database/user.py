from database.base import db
from datetime import datetime
from config import HOST, PORT


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    userAccount = db.Column(db.String(255))
    avatarUrl = db.Column(db.String(1024), default=f'http://{HOST}:{PORT}/user/avatar/default_avatar.png')
    gender = db.Column(db.Integer)
    userPassword = db.Column(db.String(512))
    phone = db.Column(db.String(128))
    email = db.Column(db.String(512))
    userStatus = db.Column(db.Integer, default=0)
    createTime = db.Column(db.DateTime, default=datetime.now())
    updateTime = db.Column(db.DateTime, default=datetime.now())
    isDelete = db.Column(db.Integer, default=0)
    userRole = db.Column(db.Integer, default=0)
    planetCode = db.Column(db.String(512))
    tags = db.Column(db.String(1024), default="[]")
    profile = db.Column(db.String(512))

    def __repr__(self):
        return '<User %r>' % self.username
