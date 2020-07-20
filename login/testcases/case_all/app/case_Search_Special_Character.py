import unittest
import json
from login.templates.app.account.Get_Logon_Token import get_app_login_token
from login.templates.utils import getconf, httputils


"""
特殊字符搜索

"""
class Case_Search_Special_Character(unittest.TestCase):
    params = {'keyWord':'',
              'searchOption':'1,2,3,4,5',
              'type':'0',
              'pageNum':'1',
              'pageSize':'5'}
    def test_search_special_character(self):
        '''特殊字符搜索'''
        self.params['token'] =get_app_login_token()#获取登录的token
        API=getconf.get_global_conf('apinames','searchBatch')#获取API名称
        r=httputils.get_app(API,parameters=self.params)

        print('返回的url为：',r.url)
        #状态校验
        self.assertEqual(r.status_code, 200, '请求失败')
        self.assertEqual(json.loads(r.text)['status'], 0, '请求失败')
        #返回值校验
        rs1=json.loads(r.text)
        print(rs1)
        for key in rs1["data"]:
            if key:#只要存在key值，则断言失败
                self.assertTrue(False,"搜索结果不为空！")
                break
            else:#不存在key值，则断言成功
                self.assertTrue(True)
                print('搜索关键字为空，结果为空:',rs1['data'])
                break
if __name__ == '__main__':
    unittest.main()
