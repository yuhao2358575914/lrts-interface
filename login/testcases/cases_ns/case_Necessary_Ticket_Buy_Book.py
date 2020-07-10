#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/4/10 14:38
# @Author  : caozhuo
# @FileName: case_Necessary_Search_Album.py
# @Software: PyCharm
"""
听读券购买有声书籍

"""
import json
import random
import unittest
from time import sleep

from login.templates.admin.activities.send_code import send_ticket_by_exchangeCode
from login.templates.admin.book.Book_Operation import operation_book_get_unbuyedcharpters_all
from login.templates.app.account.Get_Logon_Token import get_app_login_token
from login.templates.app.order.Purchase_Resources import buy_book_utils
from login.templates.users.Get_UserInfo_By_Token import get_userid_by_token
from login.templates.utils import dbutil, httputils
from login.templates.utils.confutils import getApiName


class case_Necessary_Ticket_Buy_Book(unittest.TestCase):

    def test_Necessary_Ticket_Buy_Book(self):
        '''听读券购买有声书籍'''

        token = get_app_login_token()
        user_id = get_userid_by_token(token)
        # 获取书籍
        random_int = random.randint(0, 1000)
        book = dbutil.select(
            ' SELECT book_id FROM `t_book` WHERE bState=0 AND pay_type=2 AND pay_free=1 AND price=20 AND section>300 LIMIT %d,1' % random_int,
            'db_audiobook')
        print('获取的bookid', book)
        book_id = str(book[0]['book_id'])
        # 获取未购章节
        charpters = operation_book_get_unbuyedcharpters_all(book_id, token)
        print('未购章节：', charpters)
        # 获取用户账户下的可用听读券余额，余额不够则自动发券
        data = {
            'token': token,
            'pageNum': '1',
            'pageSize': '100',
            't': '2',
            'mode': '0'
        }
        r = httputils.get_app(getApiName('ticketList'), data)
        print(r.text)
        ticket_ids = []
        json_result = json.loads(r.text)
        for i in json_result['list']:
            if i.get('balance') > 20:
                ticket_ids.append(i.get('id'))
        if len(ticket_ids) == 0:
            #如果当前用户无可用听读券，则发券
            send_ticket_by_exchangeCode('2', str(user_id))
            sleep(0.1)
            tikect = dbutil.select(
                ' SELECT id FROM `w_activity_ticket_%s` WHERE User_id=%d ORDER BY id DESC LIMIT 1' % (str(
                    user_id)[-1:], user_id),
                'db_audiobook')
            ticket_ids.append(tikect[0].get('id'))
            print('查询到的tikect_id', tikect)
        print("最终可用的tickets", ticket_ids)
        # 购买书籍
        res = buy_book_utils(token, book_id, charpters[0:1], '2', '27', '1', str(ticket_ids[0]))
        print(res)
        self.assertIsNotNone(res)


if __name__ == '__main__':
    unittest.main()
