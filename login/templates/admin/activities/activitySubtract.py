import json
import time
from login.templates.admin.account.adminlogin import login_admin
from login.templates.admin.activities.activityCommon import init_Substract_rules
from login.templates.admin.activities.activityDiscountBook import add_resources_activity
from login.templates.admin.book.Book_Operation import get_book_by_pay_type, get_albumn_by_pay_type, get_read_book_charge
from login.templates.config import constant
from login.templates.utils import httputils, confutils, dbutil, getconf
from login.templates.utils.confutils import getAdminName
from login.templates.utils.utils import get_local_time_str, get_local_time_day, get_local_time_second


def activity_Subtract_add(rangetype, rangeentitytype, Subtractcount):
    """
    添加满减待审核活动
    :param rangetype:参考constant.py
    :param rangeentitytype:参考constant.py
    :param Subtractcount：int类型
    :return:mapid
    默认添加三个满减额度，默认支持平台为安卓、ios，所有渠道，所有版本
    """
    # 登录admin获取token
    admintoken = login_admin()
    # 请求入参
    supportControl = {"province": "", "coopType": "", "channel": "",
                      "versionControl": {"androidMin": "", "androidMax": "", "iosMin": "", "iosMax": "",
                                         "appType": "1,3"}}
    # subtractRule=[{"limitFee":1000,"subtractFee":100,"showOrder":1},{"limitFee":1200,"subtractFee":200,"showOrder":2},{"limitFee":1300,"subtractFee":300,"showOrder":3}]
    subtractRule = init_Substract_rules(Subtractcount)
    title_share = '满减AT' + get_local_time_str()
    data = {
        'adTag': '满减',
        'adTagStartTime': get_local_time_day(),
        'rangeType': rangetype,
        'rangeEntityType': rangeentitytype,
        'subtractRule': str(subtractRule),
        'title': title_share,
        'detail': '',
        'startTime': get_local_time_day(),
        'endTime': get_local_time_day(2),
        'status': '5',
        'supportControl': json.dumps(supportControl),
        'showOnApp': '0',
        'showDetail': '1',
        'cover': '0'
    }
    r = httputils.postadmin(getAdminName('activitySubtractAdd'),
                            data,
                            admintoken,
                            confutils.getcurrentPath('subtract_edit'))
    print(r.text)
    if json.loads(r.text)['status'] == 0:
        res = dbutil.select('SELECT id FROM `t_activity` WHERE title= "%s"' % title_share, 'db_audiobook')
        time.sleep(0.1)
        print('满减活动id为：', str(res[0].get('id')))
        return str(res[0].get('id'))
    else:
        return json.loads(r.text)['msg']


def get_activity_Subtract_Info(activityId, admintoken):
    r = httputils.getadmin(getconf.get_global_conf('adminapis', 'activitySubtractInfo'),
                           {'id': activityId},
                           admintoken,
                           confutils.getcurrentPath('subtract_edit'))
    return json.loads(r.text)


def activity_Subtract_Edit_online(activityId):
    """
    满减活动上线
    :param activityId:为str类型活动id，来源于t_activity
    :return:
    """
    # 登录admin获取token
    admintoken = login_admin()
    # 请求入参
    res = get_activity_Subtract_Info(activityId, admintoken)
    supportControl = {"province": "", "coopType": "", "channel": "",
                      "versionControl": {"androidMin": "", "androidMax": "", "iosMin": "", "iosMax": "",
                                         "appType": "1,3"}}
    data = {
        'id': activityId,
        'adTag': res['data']['adTag'],
        'adTagStartTime': get_local_time_day(),
        'rangeType': res['data']['rangeType'],
        'rangeEntityType': res['data']['rangeEntityType'],
        'subtractRule': str(res['data']['subtractRule']),
        'title': res['data']['title'],
        'detail': '',
        'startTime': get_local_time_second(30),
        'endTime': get_local_time_day(2),
        'status': '1',
        'supportControl': json.dumps(supportControl),
        'showOnApp': '0',
        'showDetail': '1',
        'cover': '0'
    }
    r = httputils.postadmin(getconf.get_global_conf('adminapis', 'activitySubtractEdit'),
                            data,
                            admintoken,
                            confutils.getcurrentPath('subtract_edit'))
    print(r.text)
    if json.loads(r.text)['status'] == 0:
        return '满减活动"%s"上线成功！' % activityId
    else:
        return json.loads(r.text)['msg']


def add_Subtract_activity(rangeentitytype):
    """
    全流程生成可用满减活动
    其中entityIds可以根据Book_Operation.py下的get_book_by_pay_type方法获取
    :param entityIds:类型为str，例如:'2382832'或'2123232,232,323'
    :param rangetype:类型为str，参考constant.py文件
    :param rangeentitytype:类型为str，参考constant.py文件
    :return:
    """
    # 添加一个待审核的活动
    activityId = activity_Subtract_add('1', rangeentitytype, 4)
    # 将该活动上线
    activity_Subtract_Edit_online(activityId)
    # 添加资源
    if rangeentitytype == '1':
        book_charpter = get_book_by_pay_type(constant.payType_charge_charpter, 1)
        book_zhenben = get_book_by_pay_type(constant.payType_charge_whole, 1)
        book_subs = get_book_by_pay_type(constant.payType_charge_subscribe, 1)
        entityIds = ','.join([book_charpter, book_zhenben, book_subs])
        add_resources_activity(activityId, entityIds, constant.resourceType_book)
        return activityId
    elif rangeentitytype == '2':
        albumn_charpter = get_albumn_by_pay_type(constant.payType_charge_charpter, 1)
        albumn_zhenben = get_albumn_by_pay_type(constant.payType_charge_whole, 1)
        albumn_subs = get_albumn_by_pay_type(constant.payType_charge_subscribe, 1)
        entityIds = ','.join([albumn_charpter, albumn_zhenben, albumn_subs])
        add_resources_activity(activityId, entityIds, constant.resourceType_albumn)
        return activityId
    elif rangeentitytype == '3':
        books = get_read_book_charge(1)
        add_resources_activity(activityId, books, constant.resourceType_readBook)
        return activityId
