import json
import unittest

from login.templates.app.account.Get_Logon_Token import get_app_login_token
from login.templates.utils import httputils, getconf
from login.templates.utils.confutils import getApiName


class Case_Necessary_Reading_Bookstore_Page_Check(unittest.TestCase):

    def test_Reading_Bookstore_Page_Check(self):
        """阅读书城页，数据正常返回"""
        # 登录并获取token
        token = get_app_login_token()
        # 第一次请求获取资源筛选数据
        list1 = [15, 16, 17, 18, 19]
        data = {
            'token': token,
            'types': str(list1),
            'mode': '0'
        }
        # 首次请求资源筛选页数据
        r = httputils.get_app(getApiName('recommendPage'), data)
        print(r.text)
        list2 = json.loads(r.text)['list']
        self.assertTrue(len(list2) > 0)

    if __name__ == '__main__':
        unittest.main()
