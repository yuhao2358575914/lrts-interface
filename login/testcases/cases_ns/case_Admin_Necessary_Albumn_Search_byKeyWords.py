#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/4/10 14:38
# @Author  : caozhuo
# @FileName: case_Admin_Necessary_Book_Search_byKeyWords.py
# @Software: PyCharm
"""
后台节目搜索

"""
import json
import random
import unittest
from login.templates.admin.account.adminlogin import login_admin
from login.templates.utils import getconf, httputils, dbutil
from login.templates.utils.confutils import getcurrentPath, getAdminName


class case_Admin_Necessary_Albumn_Search_byKeyWords(unittest.TestCase):

    def test_Admin_Necessary_Albumn_Search_byKeyWords(self):
        """后台节目搜索"""
        # 登录并获取token
        admin_token = login_admin()
        # 获取节目
        random_int = random.randint(0, 10)
        albumn = dbutil.select(
            ' SELECT Id,NAME FROM `t_sns_ablumn` WHERE  pay_type=2 AND pay_free=1 AND STATUS=0 LIMIT %d,1' % random_int,
            'db_audiobook')
        print('获取的albumn_id', albumn)
        albumn_id = str(albumn[0]['Id'])
        albumn_name = str(albumn[0]['NAME'])
        # 第一次请求获取资源筛选数据
        data = {
            'type': '0',
            'pageNum': '1',
            'keyword': str(albumn_id),
            'searchType': '1',
            'pageSize': '20',
            't': '1'
        }
        data1 = {
            'type': '0',
            'pageNum': '1',
            'keyword': albumn_name,
            'searchType': '4',
            'pageSize': '20',
            't': '1'
        }
        # 书籍id搜索
        albumn_id_search = httputils.getadmin(getAdminName('albumSearch'), data, admin_token,
                                              getcurrentPath('AlbumList'))
        print(albumn_id_search.text)
        albumn_id_res = json.loads(albumn_id_search.text)
        self.assertTrue(albumn_id_res['status'] == 0 and albumn_id_res['searchType'] == 1)
        # 书籍名搜索
        albumn_Name_search = httputils.getadmin(getAdminName('albumSearch'), data1, admin_token,
                                                getcurrentPath('AlbumList'))
        print(albumn_Name_search.text)
        albumn_name_res = json.loads(albumn_Name_search.text)
        self.assertTrue(albumn_name_res['status'] == 0 and albumn_name_res['searchType'] == 4)


if __name__ == '__main__':
    unittest.main()
