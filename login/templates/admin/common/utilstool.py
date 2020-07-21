import datetime
import random


def auto_gen_channelID():
    """
    生成开放平台id
    :return:
    """
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    rand = random.randint(1, 100) * 9 + 100
    if month < 10:
        month = '0' + str(month)
    else:
        month = str(month)
    if day < 10:
        day = '0' + str(day)
    else:
        day = str(day)
    year = str(year)
    str1 = year[-2:] + month + day + '001' + str(rand)
    return str1


def auto_gen_referID():
    """
    生成开放平台秘钥
    :return:
    """
    H = 'abcdefghzklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-.~!@#$%^&*()_:<>?'
    salt = ''
    for i in range(24):
        salt += random.choice(H)
    return str(salt)

