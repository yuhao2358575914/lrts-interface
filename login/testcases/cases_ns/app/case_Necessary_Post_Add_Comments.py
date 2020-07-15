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


class case_Necessary_Book_Add_Comments(unittest.TestCase):

    def test_book_add_comments(self):
        """帖子添加评论"""
        # 数据准备
        Id = dbutil.select('SELECT id FROM t_group_post WHERE STATUS=0 LIMIT 1', 'db_audiobook')
        if Id:
            srcEntityId = Id[0]["id"]
        # 登录并获取token
        token = get_app_login_token()
        # 第一次请求获取资源筛选数据
        data = {
            'token': token,
            'checkType': '0',
            'commentContent': ranstr(5),
            'commentStar': '5',
            'entityType': '6',
            'fatherId': '0',
            'srcEntityId': str(srcEntityId),
            'mode': '0'
        }
        # 首次请求资源筛选页数据
        r = httputils.get_app(getconf.get_global_conf('apinames', 'AddComment.action'), data)
        print(r.text)
        commentId = json.loads(r.text)['commentId']
        self.assertTrue(commentId > 0)

    if __name__ == '__main__':
        unittest.main()
