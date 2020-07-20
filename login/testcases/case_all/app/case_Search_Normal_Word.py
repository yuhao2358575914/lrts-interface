import unittest
import json
from login.templates.app.account.Get_Logon_Token import get_app_login_token
from login.templates.utils import getconf, httputils
from login.templates.utils.utils import get_json_value_by_key, check_keyword_in_list

"""
正常搜索

"""


class Case_Search_Normal_Word(unittest.TestCase):
    params = {'keyWord': '总裁',
              'searchOption': '1,2,3,4,5',
              'type': '0',
              'pageNum': '1',
              'pageSize': '5'}

    def test_search_normal_word(self):
        '''输入字符正常搜索'''
        self.params['token'] = get_app_login_token()  # 获取登录的token
        API = getconf.get_global_conf('apinames', 'searchBatch')  # 获取API名称
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
