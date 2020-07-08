import json
import unittest

from login.templates.app.account.Get_Logon_Token import get_app_login_token
from login.templates.utils import httputils
from login.templates.utils.confutils import getApiName


class case_Necessary_TabChannlPage_Check(unittest.TestCase):

    def test_TabChannlPage_Check(self):
        """频道模块页，数据正常返回"""
        # 登录并获取token
        token = get_app_login_token()
        # 第一次请求获取资源筛选数据
        data = {
            'tabChannelId': '5353481',
            'recommendedSwitch': '0',
            'token': token,
            'mode': '0'
        }
        # 首次请求资源筛选页数据
        r = httputils.get_app(getApiName('tabChannelPage'), data)
        print(r.text)
        self.assertTrue(len(json.loads(r.text)['data']['moduleList']) > 0)

    if __name__ == '__main__':
        unittest.main()