from service.Base import base
from database import db, User


class adminService(base):
    def getAdminUser(self):
        admin = User.query.filter_by(userRole=1, isDelete=0).first()
        return admin if admin else None
