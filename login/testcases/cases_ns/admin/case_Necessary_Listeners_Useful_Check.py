#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/4/10 14:38
# @Author  : caozhuo
# @FileName: case_Admin_Necessary_Listeners_Useful_Check.py
# @Software: PyCharm
"""
请求听友会列表页面

"""
import json
import unittest
from login.templates.admin.account.adminlogin import login_admin
from login.templates.utils import httputils
from login.templates.utils.confutils import getcurrentPath, getAdminName


class case_Admin_Necessary_Listeners_Useful_Check(unittest.TestCase):

    def test_Admin_Listeners_Useful_Check(self):
        """请求听友会列表页面"""
        # 登录并获取token
        admin_token = login_admin()
        # 第一次请求获取资源筛选数据
        data = {
            'listType': '0',
            'typeCode': '2',
            'groupStatus': '1',
            'pageNum': '1',
            'pageSize': '20'
        }
        # 请求admin听单管理
        response = httputils.getadmin(getAdminName('GroupList'), data, admin_token,
                                      getcurrentPath('GroupList'))
        print(response.text)
        json_res = json.loads(response.text)
        self.assertTrue(len(json_res["list"]) > 0 and json_res["status"] == 0)

    if __name__ == '__main__':
        unittest.main()
