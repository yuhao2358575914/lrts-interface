<<<<<<< HEAD
# coding=gbk
from login.templates.admin.account.adminlogin import login_admin
from login.templates.admin.platformcopyright.Settlement_Management.Add_CopyRight import add_AudioBookCopyright, \
    add_ReadBookCopyright
from login.templates.admin.platformcopyright.common import Create_CopyrightName, Create_AnnouncerName
from login.templates.admin.platformcopyright.common.Create_PartnerName import partnerName
from login.templates.admin.platformcopyright.common.operate_mysql import billing_select, select, readbook_select
from login.templates.utils import httputils, confutils
from login.templates.utils.confutils import getAdminName
import json
=======
import datetime
import os
import re
>>>>>>> 32710e2b23b2c1a79d8b621327862c7624be5996

def add_CopyrightPartner(order):
    '''添加版权合作方(付费收听/vip会员）
    :param order 1表示付费收听 2 表示电子阅读 3表示VIP会员
    '''
    admintoken = login_admin() # 登录admin获取token
    admin_api = getAdminName('partnerEdit') # 获取partnerEdit接口
    print(admin_api)
    '''
    spTypeBook:付费收听 1表示勾选 0表示不勾选
    spTypeReadBook:电子阅读 1表示勾选 0表示不勾选
    spTypeVIP:VIP会员 1表示勾选 0表示不勾选
    spTypeComic:漫画 1表示勾选 0表示不勾选
    '''

    if order==1:
        data = {}
        book_cp = add_AudioBookCopyright()  # 获取版权信息
        book_cp_id = book_cp[0]  # 获取版权id
        print(book_cp_id,'11111111111111------------------------')
        print(type(book_cp_id))
        book_cp_name = book_cp[1]  # 获取版权name
        print(book_cp_name,'2222222222222222222222-----------------')
        print(type(book_cp_name))
        PartnerName_Record = partnerName(2)  # 生成版权合作方
        PartnerName = PartnerName_Record[0]  # 生成一个新的版权合作方名称
        PartnerName_Number = PartnerName_Record[1] #获取新的版权合作方名称后面的数字
        business={'spTypeBook':1, 'spTypeReadBook':0, 'spTypeVIP':0, 'spTypeComic':0}
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
        print(readbook_cp_id)
        print(type(readbook_cp_id))
        readbook_cp_name = readbook_cp[1]  # 获取版权name
        print(readbook_cp_name)
        print(type(readbook_cp_name))
        PartnerName_Record = partnerName(1)  # 生成版权合作方
        PartnerName = PartnerName_Record[0]  # 生成一个新的版权合作方名称
        PartnerName_Number = PartnerName_Record[1]  # 获取新的版权合作方名称后面的数字
        # business = {'spTypeBook': 0, 'spTypeReadBook': 1, 'spTypeVIP': 0, 'spTypeComic': 0}
        data['spTypeBook']=0
        data['spTypeReadBook']=1
        data['spTypeVIP']=0
        data['spTypeComic']=0
        data['readbookEntityId'] = str(readbook_cp_id)
        data['readbookEntityName'] = readbook_cp_name
        data['bookEntityId'] = ''
        data['bookEntityName'] = ''
    # elif order==3:
    #     business = {'spTypeBook': 0, 'spTypeReadBook': 0, 'spTypeVIP': 1, 'spTypeComic': 0}
    # else:
    #     business = {'spTypeBook': 0, 'spTypeReadBook': 0, 'spTypeVIP': 0, 'spTypeComic': 1}
    #接口入参
    data={'id':'',
        'channelEntityId':'',
        'channelEntityName':'',
        'annoucerEntityId':'',
        'annoucerEntityName':'',
        'comicEntityId':'',
        'comicEntityName':'',
        'partnerStatus':2,
        'canLogin':0,
        'identityCode':360724199901105698,
        'phone':15889890126,
        'qq':'',
        'email':'',
        'address':'深圳市南山区粤海街道',
        'postcode':'',
        'bankAccount':6021169878956231,
        'bankType':2,
        'bankProvince':17,
        'bankCity':285,
        'bankName':'深圳市中国银行南山分行',
        'taxType':0,
        'billType':1,
        'billCode':'',
        'buttMan':''}
    data['loginName']='zhoushichuanCP'+str(PartnerName_Number)
    data['password']=123456
    data['passwordConfirm']=123456
    data['partnerType']=1
    data['cooperatorType']=2
    data['spTypeAnnoucer']=0
    data['contactPerson']=PartnerName
    data['bankAccountName']='周同学'+str(PartnerName_Number)

    #发送post请求
    print(1111111111111)
    r = httputils.postadmin(admin_api, data, admintoken, confutils.getcurrentPath('PartnerEdit'))
    print(1111111133333333333333333333311111)
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


<<<<<<< HEAD
if __name__=='__main__':
    # add_AudioBookCopyright()
    # add_ReadBookCopyright()
    add_CopyrightPartner(1)
=======
#
# a=add_BuyShare_activity(get_book_by_pay_type(1,3),get_book_by_pay_type(2,3))
# print(a)
# params = '/yyting/page/recommendPage.action?pageVersion=v3&recommendedSwitch=0&type=2&token=JTa_wEdSIhzP1SZKF6GjFg**_gtSvJSSO3svh93sMwoQnezwJTTOmUT-m&imei=ODYzMjU0MDEwMTQwMjMz&nwt=1&q=474&mode=0&sc=67f156dc6a39b5884ab7f0c5a0c39695'
# s1 = params.split('?')[1].split('&')
# param_dict = {}
# for i in s1:
#     s2 = i.split('=')
#     if s2[0] != 'sc':
#         param_dict[s2[0]] = s2[1]
# class_name = os.path.basename(__file__)
# print(class_name)
# aa=run_test_bf('case_Search_Normal_Word.py')
# print(aa)
# print(type(aa))
# charpters = operation_book_get_unbuyedcharpters_all('92365489', 'MFyzOz-LtD7P1SZKF6GjFg**_qKkiCdyyMrjjDGxUh_yuZP2hbkAc4-6o')
# print(charpters)
# from login.templates.app.order.Entity_Price import get_entity_price_by_id
# from login.templates.users.Get_UserInfo_By_Token import get_userid_by_token
# token = 'M_2_2bkYZr7P1SZKF6GjFg**_gtSvJSSO3suJw7sB7aTQBX0Vfy9LgB7Z'
# charpters = operation_book_get_unbuyedcharpters_all('92365489', token)
# buy=operation_book_get_buyedcharpters_all('92365489', token)
# free=operation_book_get_freecharpters('92365489')
# print(charpters)
# print(buy)
# print(free)
>>>>>>> 32710e2b23b2c1a79d8b621327862c7624be5996
