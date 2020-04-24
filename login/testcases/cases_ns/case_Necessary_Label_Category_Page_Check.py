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


class Case_Necessary_Label_Category_Page_Check(unittest.TestCase):

    def test_Label_Category_Page_Check(self):
        """标签类别页，数据正常返回"""
        # 登录并获取token
        token = get_app_login_token()
        data = {
            'token': token,
            'mode': '0'
        }
        # 首次请求资源筛选页数据
        r = httputils.get_app(getconf.get_global_conf('apinames', 'typePage'), data)
        print(r.text)
        self.assertTrue(
            json.loads(r.text)['data']['ablumnTypeList'][0]['size'] > 0)

    if __name__ == '__main__':
        unittest.main()
