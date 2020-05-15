#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/4/10 14:38
# @Author  : caozhuo
# @FileName: case_Necessary_Search_Album.py
# @Software: PyCharm
"""
懒人币购买有声书籍

"""
import unittest
from login.templates.admin.book.Book_Operation import operation_book_get_unbuyedcharpters_all
from login.templates.app.account.Get_Logon_Token import get_app_login_token
from login.templates.app.order.Purchase_Resources import buy_book_utils


class case_Necessary_LazyCoins_Buy_Book(unittest.TestCase):

    def test_search_normal_word(self):
        '''懒人币购买有声书籍'''

        token = get_app_login_token()
        # 获取未购章节
        charpters = operation_book_get_unbuyedcharpters_all('92365489', token)
        #购买书籍
        res = buy_book_utils(token, '92365489', charpters[0:1], '2', '27', '0')
        self.assertIsNotNone(res)


if __name__ == '__main__':
    unittest.main()
