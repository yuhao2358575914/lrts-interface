#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/4/10 14:38
# @Author  : caozhuo
# @FileName: case_Necessary_Search_Album.py
# @Software: PyCharm
"""
评论

"""
import json
import unittest
from login.templates.app.account.Get_Logon_Token import get_app_login_token
from login.templates.utils import getconf, httputils, dbutil
from login.templates.utils.utils import ranstr


class case_Necessary_Reading_Book_Add_Comments(unittest.TestCase):

    def test_book_add_comments(self):
        """听单添加评论"""
        # 登录并获取token
        token = get_app_login_token()
        # 数据准备
        data1={
            'token': token,
            'opType': 'H',
            'referId': '0',
            'size': '4',
            'type': '4',
            'mode': '0'
        }
        r0=httputils.get_app(getconf.get_global_conf('apinames', 'getRecommendFolders'), data1)
        res=json.loads(r0.text)
        folderId=res['list'][0].get('folderId')
        print('听单Id:',folderId)
        # 第一次请求获取资源筛选数据
        data = {
            'token': token,
            'checkType': '0',
            'commentContent': ranstr(5),
            'commentStar': '5',
            'entityType': '7',
            'fatherId': '0',
            'srcEntityId': str(folderId),
            'mode': '0'
        }
        # 首次请求资源筛选页数据
        r = httputils.get_app(getconf.get_global_conf('apinames', 'AddComment.action'), data)
        print(r.text)
        commentId = json.loads(r.text)['commentId']
        self.assertTrue(commentId > 0)

    if __name__ == '__main__':
        unittest.main()
