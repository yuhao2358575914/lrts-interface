import json

from login.templates.admin.account.adminlogin import login_admin
from login.templates.admin.platform.common import Create_ChannelName
from login.templates.admin.platform.common.operate_mysql import select, billing_select
from login.templates.utils import confutils, httputils
from login.templates.utils.confutils import getAdminName


def add_ReleaseChannel(systemPlatform=2):
    '''添加发布渠道
    :param systemPlatform 系统平台 1表示ios  2表示android
    '''
    admin_token = login_admin()  # 登录admin获取token
    admin_api = getAdminName('editReleaseChannel')  # 获取editReleaseChannel接口
    print(admin_api)
    releaseChannelInfo = Create_ChannelName.releaseChannelName()  # 生成发布渠道
    releaseChannelName = releaseChannelInfo[0] #生成发布渠道名称
    releaseChannelCode = releaseChannelInfo[1]  # 生成发布渠道代号
    # 入参
    json_data = {}
    json_data['type'] = systemPlatform
    json_data['channelName'] = releaseChannelName
    json_data['channelCode'] = releaseChannelCode
    json_data['channelDesc'] = 'test'
    json_data['lanrenProduct'] = 1 #1表示选中 0表示不选中
    json_data['yayaProduct'] = 1 #1表示选中 0表示不选中
    json_data['mainChannel'] = 1 #1表示选中 0表示不选中
    json_data['coopChannel'] = 1 #1表示选中 0表示不选中
    # 发送post请求
    print(confutils.getcurrentPath('ReleaseChannelAdd'))
    r = httputils.postadmin(admin_api, json_data, admin_token, confutils.getcurrentPath('ReleaseChannelAdd'))
    if json.loads(r.text)['status'] == 0:
        ReleaseChannel_record = billing_select("select * from platform.t_copyright_channel order by id desc limit 1;")  # 查询添加后的发布渠道记录
        Releasechannel_id = ReleaseChannel_record[0]['id']  # 获取发布渠道id
        Releasechannel_name = ReleaseChannel_record[0]['name']  # 获取发布渠道名称
        print('----------','发布渠道：' +Releasechannel_name, '(id为', Releasechannel_id, ')', '添加成功！---------')
        return [Releasechannel_id, Releasechannel_name]
    else:
        print('---------添加失败!!!-----------')

if __name__=='__main__':
    add_ReleaseChannel(2)