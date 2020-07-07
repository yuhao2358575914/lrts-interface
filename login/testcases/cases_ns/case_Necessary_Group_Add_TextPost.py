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
from login.templates.app.account.Get_Logon_Token import get_app_login_token
from login.templates.utils import getconf, httputils
from login.templates.utils.utils import ranstr


class case_Necessary_Group_Add_TextPost(unittest.TestCase):

    def test__Group_Add_TextPost(self):
        """听友会发布文字帖子"""
        # 登录并获取token
        token = get_app_login_token()
        # 数据准备，查询用户是否加入听友会
        data = {
            'token': token,
            'desc': ranstr(15),
            'title': ranstr(10),
            'type': '3',
            'groupId': '28',
            'mode': '0'
        }
        # 首次请求资源筛选页数据
        r = httputils.post_app(getconf.get_global_conf('apinames', 'addGroupAudio'), data)
        print(r.text)
        contentId = json.loads(r.text)['contentId']
        entityId = json.loads(r.text)['entityId']
        self.assertTrue(contentId > 0)
        self.assertTrue(entityId > 0)

    if __name__ == '__main__':
        unittest.main()
