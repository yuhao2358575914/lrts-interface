#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/1/17 10:16
# @Author  : caozhuo
# @FileName: Get_Logon_Token.py
# @Software: PyCharm
import json

from login.templates.app.account import Get_Auto_Register_Token
from login.templates.utils import getconf, httputils
from login.templates.utils.confutils import getApiName
from login.templates.utils.encodeutils import app_account_encode
from login.templates.utils.getconf import get_conf, write_config_ini


def get_app_login_token(username=getconf.get_conf('users', 'appuser_pt'), pwd=getconf.get_conf('users', 'apppwd_pt')):
    """
    aap登录获取token
    :param username:用户名
    :param pwd:密码：加密之后的字段
    :return:token  str类型
    """
    payload = {'account': username, 'pwd': app_account_encode(pwd),
               'token': Get_Auto_Register_Token.get_auto_register_token_app()}
    init_token = get_conf('params', 'app_token')
    check_code = check_app_login_token(init_token)
    # 检查token是否存在并有效，无效则重新登录
    if check_code == 1 or username != getconf.get_conf('users', 'appuser_pt'):
        r = httputils.post_app(getconf.get_global_conf('apinames', 'ClientLogon'), payload)
        token_got = json.loads(r.text)['token']
        print('获取的token为', token_got)
        if token_got:
            write_config_ini('params', "app_token", token_got)
            return token_got
        # 如果账密登录失败，则走验证码登录
        else:
            payload2 = {
                'account': username,
                'type': '2',
                'verifyCode': '000000',
                'token': Get_Auto_Register_Token.get_auto_register_token_app(),
                'mode': '0'
            }
            r = httputils.post_app(getconf.get_global_conf('apinames', 'ClientLogon'), payload2)
            token_got2 = json.loads(r.text)['token']
            if token_got2:
                write_config_ini('params', "app_token", token_got2)
                return token_got2
    # 有效就直接拿来用
    else:
        return init_token


def check_app_login_token(token):
    r = httputils.get_app(getApiName('ClientGetUserInfo'), {'token': token})
    result = json.loads(r.text)
    if result['status'] == 0:
        return 0
    else:
        return 1
