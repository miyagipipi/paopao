from enum import Enum


class TeamStatusEnum(Enum):
    PUBLIC = 0 # 公开
    SECRET = 1 # 加密
    PRIVATE = 2 # 私有

    @classmethod
    def getEnumByValue(cls, value):
        for member in cls:
            if member.value == value:
                return member
        return None
