import datetime
def getStrCurTime_microseconds():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
def getStrCurTime():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
def getTime_accurateHours(time):
    #dt=datetime.timedelta(days=time.day, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=time.hour, weeks=0).
    return time.replace(minute=0, second=0,microsecond=0)
#    return dt.strftime('%Y-%m-%d %H:%M:%S.%f')
def getSqlStringTime(time):
    return time.strftime('%Y-%m-%d %H:%M:%S')
def convertStrToDatetime(str):
    return datetime.datetime.strptime(str,'%Y-%m-%d %H:%M:%S')
def getTimeForZhengDian(time):
    time=time.replace(second = 0)
    time=time.replace(minute=0)
    time=time.replace(microsecond = 0)
    return time
def addTimeDay(time,num):
    time += datetime.timedelta(days=num)
if(__name__=='__main__'):
    print(getTime_accurateHours(datetime.datetime.now()))