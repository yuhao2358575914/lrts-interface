
"""
听单的相关操作
"""
import json

from login.templates.app.account.Get_Logon_Token import get_app_login_token
from login.templates.users.Get_UserInfo_By_Token import get_userid_by_token
from login.templates.utils import getconf, httputils, dbutil
from login.templates.utils.confutils import getApiName
from login.templates.utils.httputils import get_app
from login.templates.utils.utils import get_local_time_day


def add_new_folder(token, folderName):
    """
    添加一个听单
    :param token str类型
    :param folderName: 传入听单的名字 str类型
    :return:返回创建的听单ID  int类型
    """
    params = {'id': '0'}  # 参数
    params['token'] =token
    params['name'] = folderName
    API = getconf.get_global_conf('apinames', 'addFolder.action')
    print(params)
    r = httputils.get_app(API, parameters=params)
    print("---",r.text)
    if json.loads(r.text)["status"]==2:
        print("听单已存在")
        return False
    elif json.loads(r.text)["status"]==5:
        print("超出限制")
        return False
    else:
        folderID = json.loads(r.text)['data']['folderId']
        return folderID
def delete_folder(token, folderID):
    """
     删除听单
     :param token: token str类型
     :param folderID: 听单ID  str类型
     :return:
     """
    params = {'id': '0'}  # 参数
    params['token'] =token
    params['folderIds'] =str(folderID)
    API = getconf.get_global_conf('apinames', 'deleteFolder.action')
    httputils.get_app(API, parameters=params)

def add_resource_folder(srcType,resource_id,folder_id):
    '''
    添加资源至听单
    :param srcType:资源类型 int类型 2是节目 3是书籍
    :param resource_id: 资源id  int类型
    :param folder_id:  听单id int类型
    :return: resource_id str类型 userid str类型
    '''
    #登录获取token
    token=get_app_login_token()
    # 获取接口
    api=getApiName('ClientAddConllection.action')
    # 数据准备
    params = {'token':token,
              'list': {"list": [{"srcType":srcType,
                                 "srcEntityId": str(resource_id),
                                 "opType": '0',
                                 "folderId": str(folder_id),
                                 "createTime":get_local_time_day()}]}}
    # 把入参中的value转换成字符串
    for key in params.keys():
        params[key] = str(params[key])
    # 请求接口
    r1 = get_app(api, params)
    result1 = r1.json()
    print(result1)
    status = result1['status']
    # 获取userid
    userid=get_userid_by_token(token)
    #userid最后两位
    userid_xx=int(userid)%50
    if userid_xx<10:
        userid_xx='0'+str(userid_xx)
    else:
        userid_xx=userid_xx
    res=dbutil.select('select * from t_collection_item_%s where folder_id=%s and src_entity_id=%s'%(userid_xx,folder_id,resource_id),'db_yyting_partdb')
    print(res)
    if status==0 and res:
        print('---------添加资源至听单成功！-----------')
        return [resource_id,str(userid)]
    else:
        print(result1['msg'] + '-----添加失败！-----')
        return False

def delete_resource_folder(srcType,resource_id,folder_id):
    '''
    删除听单中收藏的资源
    :param srcType 资源类型 2-节目 3-书籍 int类型
    :param resource_id:  资源id int类型
    :param folder_id:  听单id int类型
    :return:
    '''
    #登录获取token
    token=get_app_login_token()
    #获取api
    api=getApiName('ClientAddConllection.action')
    #入参
    params={'list':str({"list":[{"srcType":str(srcType),"srcEntityId":str(resource_id),"opType":'1',"folderId":str(folder_id)}]}),
            'token':token}
    #请求
    r=get_app(api,params)
    result=r.json()
    status=result['status']
    #数据库查询
    userid = get_userid_by_token(token) # 获取userid
    # userid最后两位
    userid_xx = int(userid) % 50
    if userid_xx < 10:
        userid_xx = '0' + str(userid_xx)
    else:
        userid_xx = userid_xx
    res = dbutil.select('select * from t_collection_item_%s where folder_id=%s and src_entity_id=%s' % (
        userid_xx, folder_id, resource_id), 'db_yyting_partdb')
    print(res)
    print(type(res))
    #校验
    if status==0 and res==():
        print('---------资源从听单中删除成功---------')
    else:
        print(result['msg'] + '-----删除失败！-----')
        return False
def get_folder_details(folderId):
    '''
    获取听单详情
    :param userid:用户id int类型
    :param folderId: 听单id int类型
    :return: 听单中的资源 list列表类型
    '''
    #登录获取token
    token=get_app_login_token()
    # 获取接口
    folder_detail_api = getApiName('getFolderEntities.action')
    # 听单详情接口入参
    folder_detail_params = {'opType': 'H', 'pageSize': '100', 'referId': '0'}
    folder_detail_params['folderId'] = str(folderId)
    folder_detail_params['userId'] = str(get_userid_by_token(token))  # 获取userid
    folder_detail_params['token'] = token
    r = get_app(folder_detail_api, folder_detail_params)  # 请求听单详情接口
    result = json.loads(r.text)  # 字符串转换成字典
    print(result)
    return [r,result]






