# coding=gbk
from login.templates.admin.account.adminlogin import login_admin

from login.templates.admin.platform.common.Add_Announcer import add_Announcer
from login.templates.admin.platform.common.Create_PartnerName import partnerName
from login.templates.admin.platform.common.Create_Number import create_PhoneNum, create_IDNumber, \
    create_CreditCardNumbers
from login.templates.admin.platform.common.operate_mysql import billing_select, select, readbook_select
from login.templates.utils import httputils, confutils
from login.templates.utils.confutils import getAdminName
import json

def add_AnchorPartner(order):
    '''添加主播合作方
    :param order 1表示付费收听 2 表示主播打赏 3 表示VIP会员
    '''
    admintoken = login_admin() # 登录admin获取token
    admin_api = getAdminName('partnerEdit') # 获取partnerEdit接口
    print(admin_api)
    data = {}
    book_cp = add_Announcer()  # 获取播音信息
    book_cp_id = book_cp[0]  # 获取播音id
    book_cp_name = book_cp[1]  # 获取播音name
    PartnerName_Record = partnerName(3)  # 生成主播合作方
    PartnerName = PartnerName_Record[0]  # 生成一个新的主播合作方名称
    PartnerName_Number = PartnerName_Record[1]  # 获取新的主播合作方名称后面的数字
    if order==1:
        # business={'spTypeBook':1, 'spTypeReadBook':0, 'spTypeVIP':0, 'spTypeComic':0}
        data['spTypeBook'] = 1
        data['spTypeReadBook'] = 0
        data['spTypeVIP'] = 0
        data['spTypeComic'] = 0
        data['spTypeAnnoucer'] = 0
        data['annoucerEntityId'] = book_cp_id
        data['annoucerEntityName'] = book_cp_name

    elif order==2:
        # business={'spTypeBook':1, 'spTypeReadBook':0, 'spTypeVIP':0, 'spTypeComic':0}
        data['spTypeBook'] = 0
        data['spTypeReadBook'] = 0
        data['spTypeVIP'] = 0
        data['spTypeComic'] = 0
        data['spTypeAnnoucer'] = 1
        data['annoucerEntityId'] = book_cp_id
        data['annoucerEntityName'] = book_cp_name
    elif order==3:
        # business={'spTypeBook':1, 'spTypeReadBook':0, 'spTypeVIP':0, 'spTypeComic':0}
        data['spTypeBook'] = 0
        data['spTypeReadBook'] = 0
        data['spTypeVIP'] = 1
        data['spTypeComic'] = 0
        data['spTypeAnnoucer'] = 0
        data['annoucerEntityId'] = book_cp_id
        data['annoucerEntityName'] = book_cp_name
    else:
        print('传参错误，请重新输入！！！')
    #接口入参
    data['id']=''
    data['bookEntityId'] = ''
    data['bookEntityName'] = ''
    data['readbookEntityId'] = ''
    data['readbookEntityName'] = ''
    data['comicEntityId'] = ''
    data['comicEntityName'] = ''
    data['channelEntityId']=''
    data['channelEntityName']=''
    data['partnerStatus']=2
    data['canLogin']=0
    data['identityCode']=create_IDNumber()
    data['phone']=create_PhoneNum()
    data['qq']=''
    data['email']=''
    data['address']='深圳市南山区粤海街道'
    data['postcode']=''
    data['bankAccount']=create_CreditCardNumbers()
    data['bankType']=1 #1表示中国银行
    data['bankProvince']=17
    data['bankCity']=285
    data['bankName']='深圳市中国银行南山分行'
    data['taxType']=0
    data['billType']=1
    data['billCode']=''
    data['buttMan']=''
    data['loginName']='zhoushichuanCP'+str(PartnerName_Number)
    data['password']=123456
    data['passwordConfirm']=123456
    data['partnerType']=1 #1表示个人账户 2表示公司账户
    data['cooperatorType']=3  #1渠道 2版权 3主播
    data['contactPerson'] = PartnerName
    data['bankAccountName'] = '周同学01'

    #发送post请求
    r = httputils.postadmin(admin_api, data, admintoken, confutils.getcurrentPath('PartnerEdit'))
    res=json.loads(r.text)
    print(res)
    if res['status']==0:
        Anchor_partner=billing_select("SELECT * from billing.p_partner ORDER BY id desc LIMIT 1;")
        Anchor_partnerId=Anchor_partner[0]['id']
        Anchor_partnerName=Anchor_partner[0]['contact_person']
        print('-----------主播合作方：'+Anchor_partnerName+'(id:'+str(Anchor_partnerId)+')'+'添加成功！！！---------------------')
        return[Anchor_partnerId,Anchor_partnerName]
    else:
        print('---------添加失败！！！-----------')


if __name__=='__main__':
    # add_AudioBookCopyright()
    # add_ReadBookCopyright()
    add_AnchorPartner(1)