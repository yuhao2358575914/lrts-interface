import json
import unittest

from login.templates.app.account.Get_Logon_Token import get_app_login_token
from login.templates.utils import httputils, getconf
from login.templates.utils.confutils import getApiName


class case_Necessary_RecommendPage_Check(unittest.TestCase):

    def test_RecommendPage_Check(self):
        """首页数据检查校验"""
        # 登录并获取token
        token = get_app_login_token()
        # 第一次请求获取资源筛选数据
        list1 = [15, 16, 17, 18, 19]
        data = {
            'pageVersion': 'v3',
            'recommendedSwitch': '1',
            'type': '2',
            'token': token,
            'mode': '0'
        }
        # 首次请求资源筛选页数据
        r = httputils.get_app(getApiName('recommendPage'), data)
        print(r.text)
        list2 = json.loads(r.text)['data']['bannerList']
        list3=json.loads(r.text)['data']['navigationBarAttach']
        self.assertTrue(len(list2) > 0 and len(list3) > 0)

    if __name__ == '__main__':
        unittest.main()
