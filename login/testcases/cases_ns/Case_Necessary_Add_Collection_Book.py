import time
import unittest
import json

from login.templates.app.account.Get_Logon_Token import get_app_login_token
from login.templates.app.common.Folder_Operation import add_new_folder, delete_folder
from login.templates.users.Get_UserInfo_By_Token import get_userid_by_token
from login.templates.utils import getconf, httputils
from login.templates.utils.utils import get_json_value_by_key

"""
收藏书籍

"""


class Case_Necessary_Add_Collection_Book(unittest.TestCase):
    params = {'list':
                  {"list": [{"srcType": '3', "srcEntityId": '', "opType": '0', "folderId": '', "createTime": ''}]}
              }

    # srcType 2是节目，3是书籍
    # srcEntityId 资源ID

    def test_case_necessary_add_collection_book(self):
        """收藏书籍"""
        token = get_app_login_token()  # 获取token
        folderID = add_new_folder(token, '我喜欢的是11')  # 添加听单的ID
        resource_ID = '30234'  # 书籍ID
        create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 当前时间
        # 设置参数
        self.params['token'] = token
        self.params['list']['list'][0]['srcEntityId'] = resource_ID  # 资源ID
        self.params['list']['list'][0]['folderId'] = str(folderID)  # 听单ID
        self.params['list']['list'][0]['createTime'] = create_time  # 创建时间
        # value值强制转换为str，因为param中嵌套了字典，字典再嵌套了列表
        for key in self.params.keys():
            self.params[key] = str(self.params[key])

        # 请求接口
        API = getconf.get_global_conf('apinames', 'ClientAddConllection.action')  # 添加的至收藏的API
        r = httputils.get_app(API, parameters=self.params)
        rs1 = json.loads(r.text)
        print(rs1)
        # 状态校验
        self.assertEqual(r.status_code, 200, '请求失败')
        self.assertEqual(rs1['status'], 0, '请求失败')

        # 验证收藏是否成功,获取听单内的资源ID，验证是否收藏成功
        user_id = get_userid_by_token(token)
        get_folder_detail_params = {'opType': 'H', 'pageSize': '100', 'referId': '0', 'userId': str(user_id),
                                    'folderId': str(folderID)}  # 获取听单资源的参数
        get_folder_detail_API = getconf.get_global_conf('apinames', 'getFolderEntities.action')  # 获取听单资源的API
        r2 = httputils.get_app(get_folder_detail_API, get_folder_detail_params)  # 获取该听单的详情
        rs2 = json.loads(r2.text)
        print(rs2)
        entityId = get_json_value_by_key(rs2, 'entityId')  # 获取资源内的ID
        self.assertIn(int(resource_ID), entityId, "ID为的资源收藏不成功！")
        delete_folder(token, folderID)  # 清除听单数据


if __name__ == '__main__':
    unittest.main()
