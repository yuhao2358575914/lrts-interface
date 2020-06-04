#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/4/10 14:38
# @Author  : caozhuo
# @FileName: case_Necessary_Advert_Recommend_Navigate.py
# @Software: PyCharm
"""
正常搜索

"""
import json
import unittest

from login.templates.app.account.Get_Logon_Token import get_app_login_token
from login.templates.utils import httputils, dbutil
from login.templates.utils.confutils import getApiName


class case_Necessary_Advert_Recommend_Navigate(unittest.TestCase):

    def test_Advert_Recommend_Navigate(self):
        '''app首页导航广告请求'''

        # 请求开屏广告
        data = {'type': '15',
                'terminalType': '1',
                'pageSize': '100',
                'pageNum': '1',
                'token': get_app_login_token(),
                'mode': '0'}
        r = httputils.get_app(getApiName('ClientAdvertList'), data)
        # # 状态校验
        self.assertEqual(json.loads(r.text)['status'], 0, '请求失败')
        response_data = json.loads(r.text)
        if response_data.get('count') > 0:
            for advert in response_data.get('list'):
                print('api请求的广告id:', advert.get('id'))
                self.assertTrue(advert.get('id'))


if __name__ == '__main__':
    unittest.main()
