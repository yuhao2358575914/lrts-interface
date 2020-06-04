#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/4/10 14:38
# @Author  : caozhuo
# @FileName: case_Necessary_Search_Album.py
# @Software: PyCharm
"""
懒人币购买节目

"""
import json
import unittest
from login.templates.admin.book.Book_Operation import operation_book_get_unbuyedcharpters_all
from login.templates.app.account.Get_Logon_Token import get_app_login_token
from login.templates.app.order.Purchase_Resources import buy_albumn_utils
from login.templates.utils import httputils, getconf


class case_Necessary_LazyCoins_Buy_Album(unittest.TestCase):

    def test_search_normal_word(self):
        '''懒人币购买节目'''

        token = get_app_login_token()
        # 获取节目未购章节
        # 第一次请求获取资源筛选数据
        data = {
            'token': token,
            'ablumnId': '402789',
            'pageNum': '1',
            'pageSize': '10000',
            'sortType': '0',
            'mode': '0'
        }
        # 首次请求资源筛选页数据
        r = httputils.get_app(getconf.get_global_conf('apinames', 'getAblumnAudios'), data)
        print(r.text)
        res = json.loads(r.text)
        audio_list = []
        for audio in res.get('list'):
            if audio['buy'] == 0 and audio['payType'] == 1:
                audio_list.append(audio.get('audioId'))
        print(audio_list)
        # 购买节目
        res = buy_albumn_utils(token, '402789', audio_list[0:1], '2', '41', '0')
        self.assertIsNotNone(res)


if __name__ == '__main__':
    unittest.main()
