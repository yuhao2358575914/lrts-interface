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


class case_Necessary_Group_Add_TextPost(unittest.TestCase):

    def test__Group_Add_TextPost(self):
        """听友会发布文字帖子"""
        # 登录并获取token
        token = get_app_login_token()
        # 数据准备，查询用户是否加入听友会
        user_id = get_userid_by_token(token)
        print('测试sql','SELECT group_id FROM t_group_user WHERE User_id=%s' % user_id)
        group_ids = dbutil.select('SELECT group_id FROM t_group_user WHERE User_id=%s' % user_id, 'db_audiobook')
        print('查询出的组id：',group_ids)
        if group_ids[0]["group_id"]:
            group_id = str(group_ids[0]["group_id"])
        else:
            data1 = {
                'groupId': '28',
                'userId': user_id,
                'token': token,
                'opType': '1',
                'mode': '0'
            }
            r1 = httputils.get_app(getconf.get_global_conf('apinames', 'addGroupAudio'), data1)
            if r1.text['status'] == 0:
                group_id = '28'
        # 第一次请求获取资源筛选数据
        data = {
            'token': token,
            'desc': ranstr(15),
            'title': ranstr(10),
            'type': '3',
            'groupId': group_id,
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
