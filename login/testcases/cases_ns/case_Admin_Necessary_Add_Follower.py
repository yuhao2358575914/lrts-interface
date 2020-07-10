#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/4/10 14:38
# @Author  : caozhuo
# @FileName: case_Necessary_Search_Album.py
# @Software: PyCharm
"""
正常搜索

"""
import json
import unittest

from login.templates.admin.book.Book_Operation import get_book_by_pay_type
from login.templates.app.account.Get_Logon_Token import get_app_login_token
from login.templates.users.Get_UserInfo_By_Token import get_userid_by_token
from login.templates.utils import getconf, httputils, dbutil
from login.templates.utils.utils import get_json_value_by_key, check_keyword_in_list, ranstr


class case_Necessary_Add_Follower(unittest.TestCase):

    def test_Add_Follower(self):
        """关注主播"""
        # 登录并获取token
        token = get_app_login_token()
        # 第一次请求获取资源筛选数据
        data = {
            'token': token,
            'needAlbum': '1',
            'needFollow': '0',
            'opType': 'H',
            'type': '1',
            'typeId': '0',
            'mode': '0'
        }
        # 首次请求资源筛选页数据
        r = httputils.get_app(getconf.get_global_conf('apinames', 'getRecommendUsers'), data)
        print(r.text)
        # 获取关注用户id
        userId = json.loads(r.text)['list'][0].get('userId')
        # 开启关注主播
        r1 = httputils.get_app(getconf.get_global_conf('apinames', 'addFollower'),
                               {'type': '1', 'userIds': str(userId), 'token': token, 'mode': '0'})
        if json.loads(r1.text)['status'] == 0:
            #取消关注主播
            r2 = httputils.get_app(getconf.get_global_conf('apinames', 'addFollower'),
                                   {'type': '1', 'userIds': str(userId), 'token': token, 'mode': '0'})
            self.assertTrue(json.loads(r2.text)['status'] == 0)

    if __name__ == '__main__':
        unittest.main()
