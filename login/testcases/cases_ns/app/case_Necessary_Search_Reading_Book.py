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
from login.templates.utils import getconf, httputils, dbutil
from login.templates.utils.confutils import getApiName
from login.templates.utils.utils import get_json_value_by_key, check_keyword_in_list


class case_Necessary_Search_Reading_Book(unittest.TestCase):
    def test_search_normal_word(self):
        '''阅读书籍搜索'''
        # 数据准备
        book_name = dbutil.select(' SELECT book_name FROM t_read_book WHERE state=1 LIMIT 1', 'db_audiobook')
        if book_name:
            search_word = book_name[0]["book_name"]
        print('******************:',book_name)
        data = {'type': '0',
                'pageNum': '1',
                'pageSize': '5',
                'token': get_app_login_token(),
                'keyWord': search_word}

        r = httputils.get_app(getApiName('readBook'), data)
        # 状态校验
        self.assertEqual(r.status_code, 200, '请求失败')
        self.assertEqual(json.loads(r.text)['status'], 0, '请求失败')
        # 返回值校验
        rs1 = json.loads(r.text)
        print(rs1)
        rec = get_json_value_by_key(rs1, 'name')  # 获取name
        print("name值：", rec)
        self.assertTrue(check_keyword_in_list(search_word, rec), '搜索结果为null')


if __name__ == '__main__':
    unittest.main()
