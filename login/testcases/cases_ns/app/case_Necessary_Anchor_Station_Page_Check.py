import json
import unittest

from login.templates.app.account.Get_Logon_Token import get_app_login_token
from login.templates.utils import httputils
from login.templates.utils.confutils import getApiName


class case_Necessary_Anchor_Station_Page_Check(unittest.TestCase):

    def test_Anchor_Station_Page_Check(self):
        """主播电台，数据正常返回"""
        # 登录并获取token
        token = get_app_login_token()
        # 第一次请求获取资源筛选数据
        data = {
            'dsize': '20',
            'entityId': '1000',
            'token': token,
            'entityType': '1',
            'pageNum': '1',
            'showFilters': '0',
            'mode': '0'
        }
        # 首次请求资源筛选页数据
        r = httputils.get_app(getApiName('filterResources'), data)
        print(r.text)
        self.assertTrue(json.loads(r.text)['albumCount'] > 0 and len(json.loads(r.text)['albums']) > 0 and len(json.loads(r.text)['albumIds']) > 0)

    if __name__ == '__main__':
        unittest.main()
