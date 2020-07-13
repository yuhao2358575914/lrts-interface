#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/4/10 14:38
# @Author  : caozhuo
# @FileName: case_Admin_Necessary_Book_Search_byKeyWords.py
# @Software: PyCharm
"""
后台阅读书籍搜索

"""
import json
import random
import unittest
from login.templates.admin.account.adminlogin import login_admin
from login.templates.utils import getconf, httputils, dbutil
from login.templates.utils.confutils import getcurrentPath, getAdminName


class case_Admin_Necessary_ReadingBook_Search_byKeyWords(unittest.TestCase):

    def test_Admin_ReadingBook_Search_byKeyWords(self):
        """后台阅读书籍搜索"""
        # 登录并获取token
        admin_token = login_admin()
        # 获取书籍
        random_int = random.randint(0, 100)
        book = dbutil.select(
            'SELECT id,book_name FROM `t_read_book` WHERE state=1 LIMIT %d,1' % random_int,
            'db_audiobook')
        print('获取的book', book)
        book_id = str(book[0]['id'])
        book_name = str(book[0]['book_name'])
        # 第一次请求获取资源筛选数据
        data = {
            'pageNum': '1',
            'keyWord': book_id,
            'freeType': '-1',
            'stateType': '-1',
            'orderType': '1',
            'searchType': '2'
        }
        data1 = {
            'pageNum': '1',
            'keyWord': book_name,
            'freeType': '-1',
            'stateType': '-1',
            'orderType': '1',
            'searchType': '1'
        }
        # 书籍id搜索
        book_id_search = httputils.getadmin(getAdminName('readBookList'), data, admin_token,
                                            getcurrentPath('ReadBookList'))
        print(book_id_search.text)
        book_id_res = json.loads(book_id_search.text)
        self.assertTrue(book_id_res['count'] == 1 and str(book_id_res['list'][0]['id']) == book_id)
        # 书籍名搜索
        book_Name_search = httputils.getadmin(getAdminName('readBookList'), data1, admin_token,
                                              getcurrentPath('ReadBookList'))
        print(book_Name_search.text)
        book_name_res = json.loads(book_Name_search.text)
        self.assertTrue(book_name in [book_name_res["list"][i]["bookName"]] for i in book_name_res["list"])

    if __name__ == '__main__':
        unittest.main()
