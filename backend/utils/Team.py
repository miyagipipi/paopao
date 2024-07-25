from common import FormatDateTime
import json


def unionTeamItem(item):
    return {
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'maxNum': item.maxNum,
        'expireTime': item.expireTime,
        'userId': item.userId,
        'status': item.status,
        'password': item.password,
        'createTime': item.createTime,
        'updateTime': item.updateTime,
        'isDelete': item.isDelete
    }


def unionTeamPlanItem(item):
    return {
        'id': item.id,
        'userId': item.userId,
        'teamId': item.teamId,
        'title': item.title,
        'description': item.description,
        'createTime': item.createTime,
        'updateTime': item.updateTime,
        'isDelete': item.isDelete
    }