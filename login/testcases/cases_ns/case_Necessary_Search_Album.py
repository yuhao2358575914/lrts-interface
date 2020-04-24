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
from login.templates.utils.utils import get_json_value_by_key, check_keyword_in_list


class case_Necessary_Search_Album(unittest.TestCase):
    params = {'type': '0',
              'pageNum': '1',
              'pageSize': '5'}
    # 数据准备
    albumn_name = dbutil.select('SELECT NAME FROM t_sns_ablumn WHERE STATUS=0 LIMIT 1', 'db_audiobook')
    if albumn_name:
        search_albumn = albumn_name[0]["NAME"][1:3]

    def test_search_normal_word(self):
        '''输入字符正常搜索节目'''
        # 获取一本在线节目
        self.params['token'] = get_app_login_token()  # 获取登录的token
        self.params['keyWord'] = self.search_albumn
        API = getconf.get_global_conf('apinames', 'searchAlbum')  # 获取API名称
        r = httputils.get_app(API, parameters=self.params)
        # 状态校验
        self.assertEqual(r.status_code, 200, '请求失败')
        self.assertEqual(json.loads(r.text)['status'], 0, '请求失败')
        # 返回值校验
        rs1 = json.loads(r.text)
        print(rs1)

        rec = get_json_value_by_key(rs1, 'name')  # 获取name
        print("name值：", rec)
        keyword = self.params['keyWord']
        self.assertTrue(check_keyword_in_list(keyword, rec), '搜索结果为null')


if __name__ == '__main__':
    unittest.main()
