import json

from login.templates.admin.account.adminlogin import login_admin
from login.templates.admin.activities.activityDiscountBook import add_resources_activity
from login.templates.config import constant
from login.templates.utils import httputils, confutils, dbutil
from login.templates.utils.confutils import getAdminName
from login.templates.utils.utils import get_local_time_str, get_local_time_day, get_local_time_second


def activity_sharelisten_add():
    """
    添加分享免费听待审核活动
    :return:
    """
    # 登录admin获取token
    admintoken = login_admin()
    # 请求入参
    supportControl = {"province": "", "coopType": "", "channel": "",
                      "versionControl": {"androidMin": "", "androidMax": "", "iosMin": "", "iosMax": "",
                                         "appType": "1,3"}}
    title_share = '免费听AT' + get_local_time_str()
    data = {
        'adTag': '分享免费',
        'adTagStartTime': get_local_time_day(),
        'title': title_share,
        'detail': '',
        'startTime': get_local_time_day(),
        'endTime': get_local_time_day(2),
        'status': '5',
        'supportControl': json.dumps(supportControl),
        'showOnApp': '0'
    }
    r = httputils.postadmin(getAdminName('activityShareListenAdd'),
                            data,
                            admintoken,
                            confutils.getcurrentPath('shareFree_edit'))
    print(r.text)
    if json.loads(r.text)['status'] == 0:
        res = dbutil.select('SELECT id FROM `t_activity` WHERE title= "%s"' % title_share, 'db_audiobook')
        return str(res[0].get('id'))
    else:
        return json.loads(r.text)['msg']


def activity_ShareListen_Edit_online(activityId):
    """
    分享免费听活动上线
    :param activityId:为str类型
    :return:
    """
    # 登录admin获取token
    admintoken = login_admin()
    # 请求入参
    supportControl = {"province": "", "coopType": "", "channel": "",
                      "versionControl": {"androidMin": "", "androidMax": "", "iosMin": "", "iosMax": "",
                                         "appType": "1,3"}}
    title_share = dbutil.select('SELECT title FROM `t_activity` WHERE id= "%s"' % activityId, 'db_audiobook')
    print('标题为：', str(title_share[0].get('title')))
    data = {
        'id': activityId,
        'adTag': '分享免费',
        'adTagStartTime': get_local_time_day(),
        'title': str(title_share[0].get('title')),
        'detail': '',
        'startTime': get_local_time_second(30),
        'endTime': get_local_time_day(2),
        'status': '1',
        'cover': '0',
        'supportControl': json.dumps(supportControl),
        'showOnApp': '0'
    }
    r = httputils.postadmin(getAdminName('activityShareListenEdit'),
                            data,
                            admintoken,
                            confutils.getcurrentPath('activityBookList'))
    print(r.text)
    if json.loads(r.text)['status'] == 0:
        return '免费听活动上线成功！'
    else:
        return json.loads(r.text)['msg']


def add_ShareListen_free_activity(entityIds):
    """
    全流程生成可用分享免费听活动
     其中entityIds可以根据Book_Operation.py下的get_book_by_pay_type方法获取
    :return:
    """
    # 添加一个待审核的活动
    activityId = activity_sharelisten_add()
    # 将该活动上线
    activity_ShareListen_Edit_online(activityId)
    # 添加书籍资源
    add_resources_activity(activityId, entityIds, constant.resourceType_book)
    # 添加节目资源
    add_resources_activity(activityId, entityIds, constant.resourceType_albumn)
