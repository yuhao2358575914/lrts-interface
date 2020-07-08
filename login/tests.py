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

def add_CopyrightPartner(order):
    '''��Ӱ�Ȩ������(��������/vip��Ա��
    :param order 1��ʾ�������� 2 ��ʾ�����Ķ� 3��ʾVIP��Ա
    '''
    admintoken = login_admin() # ��¼admin��ȡtoken
    admin_api = getAdminName('partnerEdit') # ��ȡpartnerEdit�ӿ�
    print(admin_api)
    '''
    spTypeBook:�������� 1��ʾ��ѡ 0��ʾ����ѡ
    spTypeReadBook:�����Ķ� 1��ʾ��ѡ 0��ʾ����ѡ
    spTypeVIP:VIP��Ա 1��ʾ��ѡ 0��ʾ����ѡ
    spTypeComic:���� 1��ʾ��ѡ 0��ʾ����ѡ
    '''

    if order==1:
        data = {}
        book_cp = add_AudioBookCopyright()  # ��ȡ��Ȩ��Ϣ
        book_cp_id = book_cp[0]  # ��ȡ��Ȩid
        print(book_cp_id,'11111111111111------------------------')
        print(type(book_cp_id))
        book_cp_name = book_cp[1]  # ��ȡ��Ȩname
        print(book_cp_name,'2222222222222222222222-----------------')
        print(type(book_cp_name))
        PartnerName_Record = partnerName(2)  # ���ɰ�Ȩ������
        PartnerName = PartnerName_Record[0]  # ����һ���µİ�Ȩ����������
        PartnerName_Number = PartnerName_Record[1] #��ȡ�µİ�Ȩ���������ƺ��������
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
        readbook_cp = add_ReadBookCopyright()  # ��ȡ��Ȩ��Ϣ
        readbook_cp_id = str(readbook_cp[0])  # ��ȡ��Ȩid
        print(readbook_cp_id)
        print(type(readbook_cp_id))
        readbook_cp_name = readbook_cp[1]  # ��ȡ��Ȩname
        print(readbook_cp_name)
        print(type(readbook_cp_name))
        PartnerName_Record = partnerName(1)  # ���ɰ�Ȩ������
        PartnerName = PartnerName_Record[0]  # ����һ���µİ�Ȩ����������
        PartnerName_Number = PartnerName_Record[1]  # ��ȡ�µİ�Ȩ���������ƺ��������
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
    #�ӿ����
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
        'address':'��������ɽ�������ֵ�',
        'postcode':'',
        'bankAccount':6021169878956231,
        'bankType':2,
        'bankProvince':17,
        'bankCity':285,
        'bankName':'�������й�������ɽ����',
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
    data['bankAccountName']='��ͬѧ'+str(PartnerName_Number)

    #����post����
    print(1111111111111)
    r = httputils.postadmin(admin_api, data, admintoken, confutils.getcurrentPath('PartnerEdit'))
    print(1111111133333333333333333333311111)
    res=json.loads(r.text)
    print(res)
    if res['status']==0:
        cp_partner=billing_select("SELECT * from billing.p_partner ORDER BY id desc LIMIT 1;")
        cp_partnerId=cp_partner[0]['id']
        cp_partnerName=cp_partner[0]['contact_person']
        print('-----------��Ȩ��������'+cp_partnerName+'(id:'+str(cp_partnerId)+')'+'��ӳɹ�������---------------------')
        return[cp_partnerId,cp_partnerName]
    else:
        print('---------���ʧ�ܣ�����-----------')


if __name__=='__main__':
    # add_AudioBookCopyright()
    # add_ReadBookCopyright()
    add_CopyrightPartner(1)