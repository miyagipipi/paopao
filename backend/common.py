import time
from datetime import datetime


TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

def FomatTimestamp(secs, format=TIME_FORMAT):
    localtime = time.localtime(secs)
    format_time = time.strftime(format, localtime)
    return format_time


def FomatDateStr(secs):
    timeArray = time.strptime(secs, TIME_FORMAT)
    timeStamp = int(time.mktime(timeArray))
    return timeStamp


def FormatDateTime(dt, format=TIME_FORMAT):
    return dt.strftime(format)


def FromatStrToDateTime(s, format=TIME_FORMAT):
    return datetime.strptime(s, format)
