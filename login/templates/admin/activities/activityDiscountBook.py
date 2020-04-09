import json

from login.templates.admin.account.adminlogin import login_admin
from login.templates.utils import httputils, confutils
from login.templates.utils.confutils import getAdminName


def add_resources_activity(activityId, entityIds, entityType):
    """
    活动下添加资源
    :param activityId:活动id
    :param entityIds:活动需要添加的资源id，既书籍id或节目id,支持同时添加多个，写法如：'18292,282819'
    :param entityType:活动需要添加的资源类型，参考constant.py下的‘活动添加资源类型’
    :return:
    """
    # 登录admin获取token
    admintoken = login_admin()
    # 请求入参
    data = {
        'type': '0',
        'entityType': entityType,
        'activityId': activityId,
        'entityIds': entityIds
    }
    r = httputils.postadmin(getAdminName('activityDiscountBookAdd'),
                            data,
                            admintoken,
                            confutils.getcurrentPath('activityBookList'))
    print(r.text)
    if json.loads(r.text)['status'] == 0:
        return '资源"%s"已成功添加!' % entityIds
    else:
        return json.loads(r.text)['msg']
