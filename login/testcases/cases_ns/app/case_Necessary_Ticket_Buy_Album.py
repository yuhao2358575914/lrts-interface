#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/4/10 14:38
# @Author  : caozhuo
# @FileName: case_Necessary_Search_Album.py
# @Software: PyCharm
"""
听读券购买节目

"""
import json
import random
import unittest
from time import sleep

from login.templates.admin.activities.send_code import send_ticket_by_exchangeCode
from login.templates.app.account.Get_Logon_Token import get_app_login_token
from login.templates.app.order.Purchase_Resources import buy_albumn_utils
from login.templates.users.Get_UserInfo_By_Token import get_userid_by_token
from login.templates.utils import httputils, getconf, dbutil
from login.templates.utils.confutils import getApiName


class case_Necessary_Ticket_Buy_Album(unittest.TestCase):

    def test_Ticket_Buy_Album(self):
        '''听读券购买节目'''

        token = get_app_login_token()
        user_id = get_userid_by_token(token)
        # 获取节目
        random_int = random.randint(0, 20)
        albumn = dbutil.select(
            ' SELECT Id FROM `t_sns_ablumn` WHERE  pay_type=2 AND pay_free=1 AND STATUS=0 LIMIT %d,1' % random_int,
            'db_audiobook')
        print('获取的albumn_id', albumn)
        albumn_id = str(albumn[0]['Id'])
        # 第一次请求获取资源筛选数据
        data = {
            'token': token,
            'ablumnId': albumn_id,
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
            if i.get('balance') > 100:
                ticket_ids.append(i.get('id'))
        if len(ticket_ids) == 0:
            # 如果当前用户无可用听读券，则发券
            send_ticket_by_exchangeCode('2', str(user_id))
            sleep(0.1)
            tikect = dbutil.select(
                ' SELECT id FROM `w_activity_ticket_%s` WHERE User_id=%d ORDER BY id DESC LIMIT 1' % (str(
                    user_id)[-1:], user_id),
                'db_audiobook')
            ticket_ids.append(tikect[0].get('id'))
            print('查询到的tikect_id', tikect)
        print("最终可用的tickets", ticket_ids)
        # 购买节目
        res = buy_albumn_utils(token, albumn_id, audio_list[0:1], '2', '41', '1', str(ticket_ids[0]))
        self.assertIsNotNone(res)


if __name__ == '__main__':
    unittest.main()
