#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/4/10 14:38
# @Author  : caozhuo
# @FileName: case_Admin_Necessary_Book_Search_byKeyWords.py
# @Software: PyCharm
"""
书籍榜单可用检查

"""
import json
import unittest
from login.templates.admin.account.adminlogin import login_admin
from login.templates.utils import httputils
from login.templates.utils.confutils import getcurrentPath, getAdminName


class case_Admin_Necessary_BookRank_Useful_Check(unittest.TestCase):

    def test_Admin_BookRank_Useful_Check(self):
        """书籍榜单可用检查"""
        # 登录并获取token
        admin_token = login_admin()
        # 第一次请求获取资源筛选数据
        data = {
            'rankType': '1'
        }
        # 请求admin听单管理
        response = httputils.getadmin(getAdminName('rankingsList'), data, admin_token,
                                      getcurrentPath('RankingsList'))
        print(response.text)
        json_res = json.loads(response.text)
        self.assertTrue(len(json_res["list"]) > 0 and json_res["status"] == 0)

    if __name__ == '__main__':
        unittest.main()
