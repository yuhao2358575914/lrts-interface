#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/1/10 11:29
# @Author  : caozhuo
# @FileName: User.py
# @Software: PyCharm
import json

from login.templates.utils import dbutil, httputils, getconf
from login.templates.utils.confutils import getApiName
from login.templates.utils.encodeutils import app_account_encode\
    # , rsa_encrypt
from login.templates.utils.utils import create_phone, ranstr, get_local_time_str


def check_user_valid(user_id: str):
    """
    检查用户有效性
    :param user_id: str
    :return:
    """
    type_num = user_id[-1]
    res = dbutil.select('SELECT id FROM t_user_ext_%s WHERE User_id= %s' % (type_num, user_id), 'db_audiobook')
    if res:
        return 1
    else:
        return 0


def init_register_user_by_phone():
    """
    手机号注册生成新用户
    :return: userid
    """
    autotoken = get_auto_register_token_app()
    print("自动注册token如下：\n", autotoken)
    phoneNum = create_phone()
    # phoneNum='13266710497'
    nickname = '懒人AT' + ranstr(10)
    pwd = '123456'
    verifyCode = '000000'
    data = {'token': autotoken, 'regid': 'ODYzMjU0MDEwMTQwMjMz', 'verifyCode': verifyCode,
            'pwd': app_account_encode(pwd), 'phoneNum': phoneNum, 'nickname': nickname}
    datas = check_phone_registeration(autotoken, nickname, pwd, phoneNum)
    print('校验返回值', datas)
    if datas['status'] == 0:
        r = httputils.post_app(getconf.get_global_conf('apinames', 'phoneRegister'), data)
        print('用户信息如下：', r.text)
        res = json.loads(r.text)
        res['phoneNum'] = phoneNum
        res['nickname'] = nickname
        return res
    elif datas['status'] == 483:
        return datas['msg']
    else:
        init_register_user_by_phone()


def check_phone_registeration(autotoken, nickname, pwd, phoneNum):
    """
    手机号注册检查注册信息
    :param autotoken:
    :param nickname:
    :param pwd:
    :param phoneNum:
    :return:
    """
    data = {'token': autotoken, 'pwd': pwd, 'phoneNum': phoneNum,
            'nickName': nickname}
    r = httputils.post_app(getconf.get_global_conf('apinames', 'checkPhoneRegister'), data)
    return json.loads(r.text)


# def get_auto_register_token_new():
#     """
#     安卓新版本自动注册获取token
#     :return:
#     """
#     dict_str = {"androidId": "8cec4bacd1a02815", "deviceMd5": "aa48579c6abf700fc22aeffb25674c21",
#                 "imei": "863254010140233", "imsi": "460071402367517", "key": "RVjQF98r", "mac": "02:00:4C:4F:4F:50",
#                 "nowTime": get_local_time_str(), "oaid": "", "oldImei": "ODYzMjU0MDEwMTQwMjMz",
#                 "serialNo": "bacd1a028158cec4", "umengId": "b59fa718cdb5e3b29f4f7a4bfea2f5"}
#     encript_str = rsa_encrypt(str(dict_str))
#     r = httputils.post_reg(getApiName('autoreg'), {'meta': encript_str.decode(encoding="utf-8")})
#     print(r.text)
#     if r.status_code == 200:
#         return json.loads(r.text)['token']
#     else:
#         return False


def get_auto_register_token_app():
    """
    安卓老版本自动注册获取token
    :return:
    """
    autoreg = getconf.get_global_conf('apinames', 'autoreg')
    payload = {'regid': 'NDYwMDE2NTc2MjU4MDcx', 'regmei': 'ODY2MjI5MDM1MzY5ODcz'}
    r = httputils.post_app(autoreg, payload)
    if r.status_code == 200:
        return json.loads(r.text)['token']