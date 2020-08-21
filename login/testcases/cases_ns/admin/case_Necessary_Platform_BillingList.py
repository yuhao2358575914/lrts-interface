#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import random
import unittest
from time import sleep
from login.templates.admin.account.adminlogin import login_admin
from login.templates.utils import getconf, httputils, dbutil
from login.templates.utils.confutils import getcurrentPath, getAdminName


class case_Platform_BillingList(unittest.TestCase):

    def test_platform_billingList(self):
        """结算受理列表页"""
        # 登录并获取token
        admin_token = login_admin()
        # 获取admin接口url
        BillingList=getAdminName('getBillingList')
        #获取前端页面的url
        billingList_page=getcurrentPath('partnerBillingList')
        #入参
        data={}
        #调用接口
        res=httputils.getadmin(BillingList,data,admin_token,billingList_page)
        sleep(1)
        #返回值转换成字典
        r=json.loads(res.text)
        print(r)
        #校验接口请求是否成功
        self.assertTrue(len(r['list'])>0 and r['status']==0,msg='测试失败！！！')



if __name__ == '__main__':
    unittest.main()
