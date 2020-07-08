#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/4/10 14:38
# @Author  : caozhuo
# @FileName: case_Necessary_Search_Album.py
# @Software: PyCharm
"""
懒人币购买有声书籍

"""
import random
import unittest
from login.templates.admin.book.Book_Operation import operation_book_get_unbuyedcharpters_all
from login.templates.app.account.Get_Logon_Token import get_app_login_token
from login.templates.app.order.Purchase_Resources import buy_book_utils
from login.templates.utils import dbutil


class case_Necessary_LazyCoins_Buy_Book(unittest.TestCase):

    def test_Necessary_LazyCoins_Buy_Book(self):
        '''懒人币购买有声书籍'''

        token = get_app_login_token()
        # 获取书籍
        random_int = random.randint(0, 1000)
        book = dbutil.select(
            ' SELECT book_id FROM `t_book` WHERE bState=0 AND pay_type=2 AND pay_free=1 AND price=20 AND section>300 LIMIT %d,1' % random_int,
            'db_audiobook')
        print('获取的bookid',book)
        book_id=str(book[0]['book_id'])
        # 获取未购章节
        charpters = operation_book_get_unbuyedcharpters_all(book_id, token)
        print('未购章节：', charpters)
        # 购买书籍
        res = buy_book_utils(token, book_id, charpters[0:1], '2', '27', '0')
        self.assertIsNotNone(res)


if __name__ == '__main__':
    unittest.main()
