# coding=gbk
from login.templates.admin.account.adminlogin import login_admin
from login.templates.admin.platform.common.Add_CopyRight import add_AudioBookCopyright, add_ReadBookCopyright, \
    add_ComicCopyright
from login.templates.admin.platform.common.Create_PartnerName import partnerName
from login.templates.admin.platform.common.Create_Number import create_PhoneNum, create_IDNumber, \
    create_CreditCardNumbers
from login.templates.admin.platform.common.operate_mysql import billing_select, select, readbook_select
from login.templates.utils import httputils, confutils
from login.templates.utils.confutils import getAdminName
import json

def add_CopyrightPartner(order):
    '''添加版权合作方(付费收听/vip会员）
    :param order 1表示付费收听 2 表示电子阅读 3表示VIP会员 4 表示漫画
    '''
    admintoken = login_admin() # 登录admin获取token
    admin_api = getAdminName('partnerEdit') # 获取partnerEdit接口
    print(admin_api)
    if order==1:
        data = {}
        book_cp = add_AudioBookCopyright()  # 获取版权信息
        book_cp_id = book_cp[0]  # 获取版权id
        book_cp_name = book_cp[1]  # 获取版权name
        PartnerName_Record = partnerName(2)  # 生成版权合作方
        PartnerName = PartnerName_Record[0]  # 生成一个新的版权合作方名称
        PartnerName_Number = PartnerName_Record[1] #获取新的版权合作方名称后面的数字
        # business={'spTypeBook':1, 'spTypeReadBook':0, 'spTypeVIP':0, 'spTypeComic':0}
        data['spTypeBook'] = 1
        data['spTypeReadBook'] = 0
        data['spTypeVIP'] = 0
        data['spTypeComic'] = 0
        data['readbookEntityId'] = ''
        data['readbookEntityName'] = ''
        data['bookEntityId'] = book_cp_id
        data['bookEntityName'] = book_cp_name

    elif order==2:
        data = {}
        readbook_cp = add_ReadBookCopyright()  # 获取版权信息
        readbook_cp_id = str(readbook_cp[0])  # 获取版权id
        readbook_cp_name = readbook_cp[1]  # 获取版权name
        PartnerName_Record = partnerName(2)  # 生成版权合作方
        PartnerName = PartnerName_Record[0]  # 生成一个新的版权合作方名称
        PartnerName_Number = PartnerName_Record[1]  # 获取新的版权合作方名称后面的数字
        # business = {'spTypeBook': 0, 'spTypeReadBook': 1, 'spTypeVIP': 0, 'spTypeComic': 0}
        data['spTypeBook']=0
        data['spTypeReadBook']=1
        data['spTypeVIP']=0
        data['spTypeComic']=0
        data['bookEntityId'] = ''
        data['bookEntityName'] = ''
        data['comicEntityId'] = ''
        data['comicEntityName'] = ''
        data['readbookEntityId'] = readbook_cp_id
        data['readbookEntityName'] = readbook_cp_name
    elif order==3:
        data = {}
        book_cp = add_AudioBookCopyright()  # 获取版权信息
        book_cp_id = book_cp[0]  # 获取版权id
        book_cp_name = book_cp[1]  # 获取版权name
        PartnerName_Record = partnerName(2)  # 生成版权合作方
        PartnerName = PartnerName_Record[0]  # 生成一个新的版权合作方名称
        PartnerName_Number = PartnerName_Record[1]  # 获取新的版权合作方名称后面的数字
        # business={'spTypeBook':1, 'spTypeReadBook':0, 'spTypeVIP':0, 'spTypeComic':0}
        data['spTypeBook'] = 0
        data['spTypeReadBook'] = 0
        data['spTypeVIP'] = 1
        data['spTypeComic'] = 0
        data['readbookEntityId'] = ''
        data['readbookEntityName'] = ''
        data['comicEntityId'] = ''
        data['comicEntityName'] = ''
        data['bookEntityId'] = book_cp_id
        data['bookEntityName'] = book_cp_name
    elif order==4:
        data = {}
        comic_cp = add_ComicCopyright()  # 获取版权信息
        comic_cp_id = str(comic_cp[0])  # 获取版权id
        comic_cp_name = comic_cp[1]  # 获取版权name
        PartnerName_Record = partnerName(2)  # 生成版权合作方
        PartnerName = PartnerName_Record[0]  # 生成一个新的版权合作方名称
        PartnerName_Number = PartnerName_Record[1]  # 获取新的版权合作方名称后面的数字
        # business = {'spTypeBook': 0, 'spTypeReadBook': 1, 'spTypeVIP': 0, 'spTypeComic': 0}
        data['spTypeBook'] = 0
        data['spTypeReadBook'] = 0
        data['spTypeVIP'] = 0
        data['spTypeComic'] = 1
        data['readbookEntityId'] = ''
        data['readbookEntityName'] = ''
        data['bookEntityId'] = ''
        data['bookEntityName'] = ''
        data['comicEntityId'] = comic_cp_id
        data['comicEntityName'] = comic_cp_name
    else:
        print('传参错误，请重新输入！！！')
    #接口入参
    data['id']=''
    data['channelEntityId']=''
    data['channelEntityName']=''
    data['annoucerEntityId']=''
    data['annoucerEntityName']=''
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
    data['cooperatorType']=2 #1渠道 2版权 3主播
    data['spTypeAnnoucer']=0
    data['contactPerson'] = PartnerName
    data['bankAccountName'] = '周同学01'

    #发送post请求
    r = httputils.postadmin(admin_api, data, admintoken, confutils.getcurrentPath('PartnerEdit'))
    res=json.loads(r.text)
    print(res)
    if res['status']==0:
        cp_partner=billing_select("SELECT * from billing.p_partner ORDER BY id desc LIMIT 1;")
        cp_partnerId=cp_partner[0]['id']
        cp_partnerName=cp_partner[0]['contact_person']
        print('-----------版权合作方：'+cp_partnerName+'(id:'+str(cp_partnerId)+')'+'添加成功！！！---------------------')
        return[cp_partnerId,cp_partnerName]
    else:
        print('---------添加失败！！！-----------')


if __name__=='__main__':
    # add_AudioBookCopyright()
    # add_ReadBookCopyright()
    add_CopyrightPartner(1)
    add_CopyrightPartner(2)
    add_CopyrightPartner(3)
    add_CopyrightPartner(4)