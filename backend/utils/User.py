from common import FormatDateTime
import json


def unionUserItem(user):
    return {
        'id': user.id,
        'username': user.username,
        'userAccount': user.userAccount,
        'avatarUrl': user.avatarUrl,
        'gender': user.gender,
        'userPassword': user.userPassword,
        'phone': user.phone,
        'email': user.email,
        'userStatus': user.userStatus,
        'createTime': FormatDateTime(user.createTime),
        'updateTime': FormatDateTime(user.updateTime),
        'isDelete': user.isDelete,
        'userRole': user.userRole,
        'planetCode': user.planetCode,
        'tags': json.loads(user.tags),
        'profile': user.profile
    }
