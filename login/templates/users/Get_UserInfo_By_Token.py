"""
获取用户信息
"""
import json

#根据token获取用户id
from login.templates.utils import httputils, getconf


def get_userid_by_token(token):
    """
    根据token获取用户id
    :param token:  str类型
    :return:  userid  int类型
    """
    r=httputils.get_app(getconf.get_global_conf('apinames','ClientGetUserInfo'),{'token':token})
    print('用户信息如下：',r.text)
    return json.loads(r.text)['userId']

#根据token获取听读券余额
def get_ticketBalance_by_token(token):
    """
    根据token获取听读券余额
    :param token:
    :return:
    """
    r=httputils.get_app(getconf.get_global_conf('apinames','ClientGetUserInfo'),{'token':token})
    return float(json.loads(r.text)['ticketBalance'])

#根据token获取用户昵称
def get_nickname_by_token(token):
    """
    根据token获取用户昵称
    :param token:
    :return:
    """
    r=httputils.get_app(getconf.get_global_conf('apinames','ClientGetUserInfo'),{'token':token})
    if json.loads(r.text)['status']==0:
        return json.loads(r.text)['nickname']
def get_user_isVip(token):
    """
    根据token判断用户是不是vip
    :param token:
    :return:
    """
    r=httputils.get_app(getconf.get_global_conf('apinames','ClientGetUserInfo'),{'token':token})
    if str(json.loads(r.text)['isV']) == '2':
        return 1
    else:
        return 0