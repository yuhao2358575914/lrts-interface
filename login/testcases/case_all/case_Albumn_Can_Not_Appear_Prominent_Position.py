import json
import unittest
from time import sleep
from login.templates.app.account.Get_Logon_Token import get_app_login_token
from login.templates.utils import httputils, getconf
from login.templates.utils.utils import del_dict_key_value_by_list
from login.templates.admin.albumn.Albumn_Operation import edit_album_info_by_dict


class case_Albumn_Can_Not_Appear_Prominent_Position(unittest.TestCase):
    def test_Albumn_Can_Not_Appear_Prominent_Position(self):
        '''节目A勾选【不能出现在筛选页显著位置】，分类筛选页中，资源A在服务器返回一页数据中的最后一条'''
        #登录并获取token
        token=get_app_login_token()
        #第一次请求获取资源筛选数据
        data={
                'token':token,
                'dsize':'20',
                'entityId':'1000',
                'entityType':'1',
                'labelIds':'0,0,0,10008,31000',
                'pageNum':'1',
                'showFilters':'0'
               }
        #首次请求资源筛选页数据
        r=httputils.get_app(getconf.get_global_conf('apinames','filterResources'), data)
        print(r.text)
        reslist=json.loads(r.text)['albumIds']
        print('第一排位的节目为：',reslist[0])
        #设置第一排位资源审核等级为：不可出现在筛选页显著位置
        msg=edit_album_info_by_dict(str(reslist[0]),{'canNotImportantShow':'true'})
        print('修改结果',msg)
        sleep(5)
        #再次请求资源筛选页数据
        r1 = httputils.get_app(getconf.get_global_conf('apinames', 'filterResources'),del_dict_key_value_by_list(data,['sc','imei','nwt','q']))
        print('再次请求返回数据',r1.text)
        reslist1 = json.loads(r1.text)['albumIds']
        print('第一排位的节目为：', reslist1[0])
        self.assertNotEqual(reslist1[0],reslist[0],'两次返回首位数据一致，资源筛选设置未生效')
if __name__ == '__main__':
    unittest.main()
