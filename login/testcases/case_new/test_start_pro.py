import os

from login.templates.app.account.Get_Logon_Token import get_app_login_token
from login.templates.utils import getconf, httputils
import json
import traceback
from login.templates.utils.utils import get_local_time_second


def test_case_mpro():
    """
    方法注释
    :return:
    """
    case_name = os.path.basename(__file__)

    try:
        token = get_app_login_token()
        # 第一次请求获取资源筛选数据
        data = {
            'token': token,
            'needAlbum': '1',
            'needFollow': '0',
            'opType': 'H',
            'type': '1',
            'typeId': '0',
            'mode': '0'
        }
        # 首次请求资源筛选页数据
        r = httputils.get_app(getconf.get_global_conf('apinames', 'getRecommendUsers'), data)
        print(r.text)
        # 获取关注用户id
        userId = json.loads(r.text)['list'][0].get('userId')
        # 开启关注主播
        r1 = httputils.get_app(getconf.get_global_conf('apinames', 'addFollower'),
                               {'type': '1', 'userIds': str(userId), 'token': token, 'mode': '0'})
        # print('状态值：', json.loads(r1.text)['status'])
        if json.loads(r1.text)['status'] == 0:
            # 取消关注主播
            r2 = httputils.get_app(getconf.get_global_conf('apinames', 'addFollower'),
                                   {'type': '2', 'userIds': str(userId), 'token': token, 'mode': '0'})
            # json_res = {}
            if json.loads(r2.text)['status'] == 0:
                json_res = {'result': '1', 'response': json.loads(r2.text), 'case_name': case_name}
                return json_res
            else:
                json_res = {'result': '0', 'response': json.loads(r2.text), 'case_name': case_name}
                return json_res
        else:
            json_res = {'result': '0', 'response': json.loads(r1.text), 'case_name': case_name}
            return json_res
    except Exception as e:
        print(str(e))
        print(repr(e))
        # print(e.message)
        print('堆栈信息', traceback.print_exc())
        print('堆栈信息2', traceback.format_exc())
        return {'result': '0', 'response': traceback.format_exc(), 'case_name': case_name}


# print('返回结果', test_case_mpro())
