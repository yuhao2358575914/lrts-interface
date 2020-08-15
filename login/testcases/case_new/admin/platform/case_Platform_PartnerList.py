#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import random
import unittest
from login.templates.admin.account.adminlogin import login_admin
from login.templates.utils import getconf, httputils, dbutil
from login.templates.utils.confutils import getcurrentPath, getAdminName


class case_Platform_PartnerList(unittest.TestCase):

    def test_platform_partnerList(self):
        """分成合作方列表页"""
        # 登录并获取token
        admin_token = login_admin()
        # 获取admin接口url
        partnerList=getAdminName('partnerList')
        #获取前端页面的url
        partnerList_page=getcurrentPath('PartnerList')
        #入参
        data={}
        #调用接口
        res=httputils.getadmin(partnerList,data,admin_token,partnerList_page)
        #返回值转换成字典
        r=json.loads(res.text)
        print(r)
        #校验接口请求是否成功
        self.assertTrue(len(r['list'])>0 and r['status']==0,msg='测试失败！！！')
    def test_platform_partnerList_channel(self):
        """分成合作方(渠道）列表页"""
        # 登录并获取token
        admin_token = login_admin()
        # 获取admin接口url
        partnerList=getAdminName('partnerList')
        #获取前端页面的url
        partnerList_page=getcurrentPath('PartnerListChannel')
        #入参
        data={'pageNum': '1',
            'pageSize': '20',
            'cooperatorType': '1'}
        #调用接口
        res=httputils.getadmin(partnerList,data,admin_token,partnerList_page)
        #返回值转换成字典
        r=json.loads(res.text)
        print(r)
        #校验接口请求是否成功
        self.assertTrue(len(r['list'])>0 and r['status']==0,msg='测试失败！！！')
    def test_platform_partnerList_copyright(self):
        """分成合作方(版权）列表页"""
        # 登录并获取token
        admin_token = login_admin()
        # 获取admin接口url
        partnerList=getAdminName('partnerList')
        #获取前端页面的url
        partnerList_page=getcurrentPath('PartnerListCopyright')
        #入参
        data={'pageNum': '1',
            'pageSize': '20',
            'cooperatorType': '2'}
        #调用接口
        res=httputils.getadmin(partnerList,data,admin_token,partnerList_page)
        #返回值转换成字典
        r=json.loads(res.text)
        print(r)
        #校验接口请求是否成功
        self.assertTrue(len(r['list'])>0 and r['status']==0,msg='测试失败！！！')
    def test_platform_partnerList_Anch(self):
        """分成合作方(主播）列表页"""
        # 登录并获取token
        admin_token = login_admin()
        # 获取admin接口url
        partnerList=getAdminName('partnerList')
        #获取前端页面的url
        partnerList_page=getcurrentPath('PartnerListAnchor')
        #入参
        data={'pageNum': '1',
            'pageSize': '20',
            'cooperatorType':'3'}
        #调用接口
        res=httputils.getadmin(partnerList,data,admin_token,partnerList_page)
        #返回值转换成字典
        r=json.loads(res.text)
        print(r)
        #校验接口请求是否成功
        self.assertTrue(len(r['list'])>0 and r['status']==0,msg='测试失败！！！')


if __name__ == '__main__':
    unittest.main()
