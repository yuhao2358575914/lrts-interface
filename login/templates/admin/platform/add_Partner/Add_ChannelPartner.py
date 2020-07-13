# coding=gbk
import random

from login.templates.admin.account.adminlogin import login_admin
from login.templates.admin.platform.common.Add_ReleaseDivideChannel import add_DivideChannel
from login.templates.admin.platform.common.Create_PartnerName import partnerName
from login.templates.admin.platform.common.Create_Number import create_PhoneNum, create_IDNumber, \
    create_CreditCardNumbers
from login.templates.admin.platform.common.operate_mysql import billing_select, select
from login.templates.utils import httputils, confutils
from login.templates.utils.confutils import getAdminName
import json

from login.templates.utils.httputils import getadmin


def add_ChannelPartner(business, partnerType):
    '''添加渠道合作方
    :param business 0表示勾选全部业务 1表示付费收听 2 表示电子阅读 3 表示主播打赏 4表示VIP会员 5表示漫画
    :param partnerType 1表示个人账户 2表示公司账户
    '''
    admintoken = login_admin()  # 登录admin获取token
    admin_api = getAdminName('partnerEdit')  # 获取partnerEdit接口
    print(admin_api)
    # 数据准备
    data = {}
    channelInfo = add_DivideChannel()  # 获取渠道信息
    channel_id = channelInfo[0]  # 获取渠道id
    channel_name = channelInfo[1]  # 获取渠道name
    # channel_id = 5039  # 获取渠道id
    # channel_name = 'IOS测试渠道'  # 获取渠道name
    PartnerName_Record = partnerName(1)  # 生成渠道合作方
    PartnerName = PartnerName_Record[0]  # 生成一个新的渠道合作方名称
    PartnerName_Number = PartnerName_Record[1]  # 获取新的版权合作方名称后面的数字
    # 判断是个人账户还是公司账户
    if partnerType == 1:
        data['contactPerson'] = PartnerName + '(个人账户)'
    elif partnerType == 2:
        data['fullName'] = PartnerName + '(公司账户)'
        data['shortName'] = PartnerName + '(公司账户)'
        data['contactPerson'] = PartnerName + '(公司账户)'
        data['deductTaxRate'] = random.randint(2, 20)
    else:
        print('账户类型输入有误！！！')
    if business == 0:
        data['spTypeBook'] = 1
        data['spTypeReadBook'] = 1
        data['spTypeVIP'] = 1
        data['spTypeComic'] = 1
        data['spTypeAnnoucer'] = 1
        data['channelEntityId'] = channel_id
        data['channelEntityName'] = channel_name
    elif business == 1:
        data['spTypeBook'] = 1
        data['spTypeReadBook'] = 0
        data['spTypeVIP'] = 0
        data['spTypeComic'] = 0
        data['spTypeAnnoucer'] = 0
        data['channelEntityId'] = channel_id
        data['channelEntityName'] = channel_name
    elif business == 2:
        data['spTypeBook'] = 0
        data['spTypeReadBook'] = 1
        data['spTypeVIP'] = 0
        data['spTypeComic'] = 0
        data['spTypeAnnoucer'] = 0
        data['channelEntityId'] = channel_id
        data['channelEntityName'] = channel_name
    elif business == 3:
        data['spTypeBook'] = 0
        data['spTypeReadBook'] = 0
        data['spTypeVIP'] = 0
        data['spTypeComic'] = 0
        data['spTypeAnnoucer'] = 1
        data['channelEntityId'] = channel_id
        data['channelEntityName'] = channel_name
    elif business == 4:
        data['spTypeBook'] = 0
        data['spTypeReadBook'] = 0
        data['spTypeVIP'] = 1
        data['spTypeComic'] = 0
        data['spTypeAnnoucer'] = 0
        data['channelEntityId'] = channel_id
        data['channelEntityName'] = channel_name
    elif business == 5:
        data['spTypeBook'] = 0
        data['spTypeReadBook'] = 0
        data['spTypeVIP'] = 0
        data['spTypeComic'] = 1
        data['spTypeAnnoucer'] = 0
        data['channelEntityId'] = channel_id
        data['channelEntityName'] = channel_name
    else:
        print('传参错误，请重新输入！！！')
    # 接口入参
    data['id'] = ''
    data['readbookEntityId'] = ''
    data['readbookEntityName'] = ''
    data['comicEntityId'] = ''
    data['comicEntityName'] = ''
    data['bookEntityId'] = ''
    data['bookEntityName'] = ''
    data['annoucerEntityId'] = ''
    data['annoucerEntityName'] = ''
    data['partnerStatus'] = 2
    data['canLogin'] = 0
    data['identityCode'] = create_IDNumber()
    data['phone'] = create_PhoneNum()
    data['qq'] = ''
    data['email'] = ''
    data['address'] = '深圳市南山区粤海街道'
    data['postcode'] = ''
    data['bankAccount'] = create_CreditCardNumbers()
    data['bankType'] = 1  # 1表示中国银行
    data['bankProvince'] = 17
    data['bankCity'] = 285
    data['bankName'] = '深圳市中国银行南山分行'
    data['taxType'] = 0
    data['billType'] = 1
    data['billCode'] = ''
    data['buttMan'] = ''
    data['loginName'] = 'zhoushichuanCh' + str(PartnerName_Number)
    data['password'] = 123456
    data['passwordConfirm'] = 123456
    data['partnerType'] = partnerType  # 1表示个人账户 2表示公司账户
    data['cooperatorType'] = 1  # 1渠道 2版权 3主播
    data['bankAccountName'] = '周同学01'

    # 发送post请求
    r = httputils.postadmin(admin_api, data, admintoken, confutils.getcurrentPath('PartnerEdit'))
    res = json.loads(r.text)
    print(res)
    if res['status'] == 0:
        Channel_partner = billing_select("SELECT * from billing.p_partner order by id desc LIMIT 1;", "billing")
        Channel_partnerId = Channel_partner[0]['id']
        Channel_partnerName = Channel_partner[0]['full_name']
        print('-----------渠道合作方：' + Channel_partnerName + '(id:' + str(
            Channel_partnerId) + ')' + '添加成功！！！---------------------')
        return [Channel_partnerId, Channel_partnerName]
    else:
        print('---------添加失败！！！-----------')


def check_information(business, partnerType):
    '''分成合作方资料审核
    :param business 0表示勾选全部业务 1表示付费收听 2 表示电子阅读 3 表示主播打赏 4表示VIP会员 5表示漫画
    '''
    admintoken = login_admin()
    admin_api = getAdminName('partnerConfirmEdit')  # 获取接口
    # 入参
    Anchor_partner = add_ChannelPartner(business, partnerType)  # 获取主播合作方id和名称
    Anchor_partnerId = Anchor_partner[0]  # 获取主播合作方id
    Anchor_partnerName = Anchor_partner[1]  # 获取主播合作方名称
    data = {}
    data['id'] = str(Anchor_partnerId)
    data['partnerStatus'] = '0'
    # 发送get请求
    res = getadmin(admin_api, data, admintoken, confutils.getcurrentPath('PartnerList'))
    r = json.loads(res.text)
    print(r)
    if r['status'] == 0:
        print('--------渠道合作方：' + Anchor_partnerName + '(id:' + str(Anchor_partnerId) + ')' + '资源审核通过！！-----------')
    else:
        print('--------渠道合作方资源审核失败！！-----------')
