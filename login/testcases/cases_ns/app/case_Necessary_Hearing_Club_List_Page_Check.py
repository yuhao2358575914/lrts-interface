from login.templates.app.account.Get_Logon_Token import get_app_login_token
import json
import unittest

from login.templates.admin.book.Book_Operation import get_book_by_pay_type
from login.templates.app.account.Get_Logon_Token import get_app_login_token
from login.templates.users.Get_UserInfo_By_Token import get_userid_by_token
from login.templates.utils import getconf, httputils, dbutil
from login.templates.utils.utils import get_json_value_by_key, check_keyword_in_list, ranstr


class case_Necessary_Hearing_Club_List_Page_Check(unittest.TestCase):

    def test__Hearing_Club_List_Page_Check(self):
        """听友会列表页，数据正常返回"""
        # 登录并获取token
        token = get_app_login_token()
        # 数据准备，查询用户是否加入听友会

        data = {
            'token': token,
            'opType': 'H',
            'referId': '0',
            'type': '2',
            'size': '20',
            'mode': '0'
        }
        # 首次请求资源筛选页数据
        r = httputils.post_app(getconf.get_global_conf('apinames', 'getRecommendList'), data)
        print(r.text)
        res = json.loads(r.text)
        self.assertTrue(res['status'] == 0)
        self.assertTrue(len(res['list']) > 0)
        self.assertTrue(res['list'][0].get('groupName') == '懒人大厅')

    if __name__ == '__main__':
        unittest.main()
