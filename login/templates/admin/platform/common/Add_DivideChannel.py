import json
from time import sleep

from login.templates.admin.account.adminlogin import login_admin
from login.templates.admin.platform.common import Create_ChannelName
from login.templates.admin.platform.common.Add_ReleaseChannel import add_ReleaseChannel
from login.templates.admin.platform.common.operate_mysql import select, billing_select
from login.templates.utils import confutils, httputils
from login.templates.utils.confutils import getAdminName


def add_DivideChannel():
    '''添加分成渠道
    '''
    admin_token = login_admin()  # 登录admin获取token
    admin_api = getAdminName('shareFeeChannelEdit')  # 获取editReleaseChannel接口
    print(admin_api)
    divideChannelInfo = Create_ChannelName.divideChannelName()  # 生成分成渠道
    divideChannelNickName = divideChannelInfo[0] #生成分成渠道简称
    divideChannelFullName = divideChannelInfo[1]  # 生成分成渠道全称
    releaseChannelInfo=add_ReleaseChannel() #获取发布渠道的信息
    releaseChannelId=releaseChannelInfo[0]  #获取发布渠道id
    releaseChannelName=releaseChannelInfo[1] #获取发布渠道名称
    # 入参
    json_data = {}
    json_data['id'] =''
    json_data['type'] = 1
    json_data['nickName'] = divideChannelNickName
    json_data['fullName'] = divideChannelFullName
    json_data['referChannelId'] =releaseChannelId
    json_data['referChannelName'] =releaseChannelName
    json_data['referKey'] = 123456
    json_data['channelStatus'] = 1
    json_data['website']=''
    json_data['description']='test'
    json_data['contactId']=''
    json_data['contactName']='周同学001'
    json_data['contactPhone']=15812345678
    json_data['contactQq']=''
    json_data['contactEmail']=''
    json_data['contactAddress']=''
    json_data['lanrenProduct']=1
    json_data['yayaProduct']=0
    # 发送post请求
    print(confutils.getcurrentPath('ShareFeeChannel'))
    r = httputils.postadmin(admin_api, json_data, admin_token, confutils.getcurrentPath('ShareFeeChannel'))
    if json.loads(r.text)['status'] == 0:
        DivideChannel_record = billing_select("select * from billing.p_share_fee_channel where product_type=1 order by id desc limit 1;")  # 查询添加后的分成渠道记录
        sleep(3)
        Dividechannel_id = DivideChannel_record[0]['id']  # 获取分成渠道id
        Dividechannel_name = DivideChannel_record[0]['full_name']  # 获取分成渠道全称
        print('----------', '分成渠道：'+Dividechannel_name, '(id为', Dividechannel_id, ')', '添加成功！---------')
        return [Dividechannel_id, Dividechannel_name]
    else:
        print('---------添加失败!!!-----------')

if __name__=='__main__':
    add_DivideChannel()