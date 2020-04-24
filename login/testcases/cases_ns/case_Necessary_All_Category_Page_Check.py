#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/4/10 14:38
# @Author  : caozhuo
# @FileName: case_Necessary_Search_Album.py
# @Software: PyCharm
"""
排行榜

"""
import json
import unittest

from login.templates.admin.book.Book_Operation import get_albumn_by_pay_type
from login.templates.app.account.Get_Logon_Token import get_app_login_token
from login.templates.utils import getconf, httputils, dbutil
from login.templates.utils.utils import get_json_value_by_key, check_keyword_in_list, ranstr


class Case_Necessary_All_Category_Page_Check(unittest.TestCase):

    def test_All_Category_Page_Check(self):
        """所有分类页，数据正常返回"""
        # 登录并获取token
        token = get_app_login_token()
        data = {
            'token': token,
            'dsize': '20',
            'entityId': '9008',
            'entityType': '1',
            'labelIds': '0,0,31000,0,10009',
            'pageNum': '1',
            'showFilters': '0',
            'mode': '0'
        }
        # 首次请求资源筛选页数据
        r = httputils.get_app(getconf.get_global_conf('apinames', 'filterResources'), data)
        print(r.text)
        self.assertTrue(json.loads(r.text)['bookIds'][0] == json.loads(r.text)['books'][0]['id'])
        tags=json.loads(r.text)['books'][0]['tags']
        self.assertTrue('会员' in str(tags))

    if __name__ == '__main__':
        unittest.main()
