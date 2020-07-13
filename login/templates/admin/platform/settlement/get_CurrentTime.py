import time

def getCurrentTime():
    '''获取当前的时间的年月日'''
    currentDate=time.strftime("%Y-%m-%d", time.localtime())
    currentMonth_style1=time.strftime("%Y-%m", time.localtime())
    currentMonth_style2=time.strftime("%Y%m", time.localtime())
    return [currentDate,currentMonth_style1,currentMonth_style2]
def month_days(date='202006'):
    '''获取当前月份的天数'''
    date=str(date)
    years=int(date[0:4])
    month=int(date[5:6])
    if (years % 4 == 0 and years % 100 != 0) or (years % 400 == 0):
        if month in [1,3,5,7,8,10,12]:
            month_days=31
        elif month in [4,6,9,11]:
            month_days=30
        else:
            month_days=29
    else:
        if month in [1, 3, 5, 7, 8, 10, 12]:
            month_days = 31
        elif month in [4, 6, 9, 11]:
            month_days = 30
        else:
            month_days = 28
    return month_days



if __name__=='__main__':
    getCurrentTime()