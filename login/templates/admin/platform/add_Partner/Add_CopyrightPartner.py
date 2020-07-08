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
    '''��Ӱ�Ȩ������(��������/vip��Ա��
    :param order 1��ʾ�������� 2 ��ʾ�����Ķ� 3��ʾVIP��Ա 4 ��ʾ����
    '''
    admintoken = login_admin() # ��¼admin��ȡtoken
    admin_api = getAdminName('partnerEdit') # ��ȡpartnerEdit�ӿ�
    print(admin_api)
    if order==1:
        data = {}
        book_cp = add_AudioBookCopyright()  # ��ȡ��Ȩ��Ϣ
        book_cp_id = book_cp[0]  # ��ȡ��Ȩid
        book_cp_name = book_cp[1]  # ��ȡ��Ȩname
        PartnerName_Record = partnerName(2)  # ���ɰ�Ȩ������
        PartnerName = PartnerName_Record[0]  # ����һ���µİ�Ȩ����������
        PartnerName_Number = PartnerName_Record[1] #��ȡ�µİ�Ȩ���������ƺ��������
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
        readbook_cp = add_ReadBookCopyright()  # ��ȡ��Ȩ��Ϣ
        readbook_cp_id = str(readbook_cp[0])  # ��ȡ��Ȩid
        readbook_cp_name = readbook_cp[1]  # ��ȡ��Ȩname
        PartnerName_Record = partnerName(2)  # ���ɰ�Ȩ������
        PartnerName = PartnerName_Record[0]  # ����һ���µİ�Ȩ����������
        PartnerName_Number = PartnerName_Record[1]  # ��ȡ�µİ�Ȩ���������ƺ��������
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
        book_cp = add_AudioBookCopyright()  # ��ȡ��Ȩ��Ϣ
        book_cp_id = book_cp[0]  # ��ȡ��Ȩid
        book_cp_name = book_cp[1]  # ��ȡ��Ȩname
        PartnerName_Record = partnerName(2)  # ���ɰ�Ȩ������
        PartnerName = PartnerName_Record[0]  # ����һ���µİ�Ȩ����������
        PartnerName_Number = PartnerName_Record[1]  # ��ȡ�µİ�Ȩ���������ƺ��������
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
        comic_cp = add_ComicCopyright()  # ��ȡ��Ȩ��Ϣ
        comic_cp_id = str(comic_cp[0])  # ��ȡ��Ȩid
        comic_cp_name = comic_cp[1]  # ��ȡ��Ȩname
        PartnerName_Record = partnerName(2)  # ���ɰ�Ȩ������
        PartnerName = PartnerName_Record[0]  # ����һ���µİ�Ȩ����������
        PartnerName_Number = PartnerName_Record[1]  # ��ȡ�µİ�Ȩ���������ƺ��������
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
        print('���δ������������룡����')
    #�ӿ����
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
    data['address']='��������ɽ�������ֵ�'
    data['postcode']=''
    data['bankAccount']=create_CreditCardNumbers()
    data['bankType']=1 #1��ʾ�й�����
    data['bankProvince']=17
    data['bankCity']=285
    data['bankName']='�������й�������ɽ����'
    data['taxType']=0
    data['billType']=1
    data['billCode']=''
    data['buttMan']=''
    data['loginName']='zhoushichuanCP'+str(PartnerName_Number)
    data['password']=123456
    data['passwordConfirm']=123456
    data['partnerType']=1 #1��ʾ�����˻� 2��ʾ��˾�˻�
    data['cooperatorType']=2 #1���� 2��Ȩ 3����
    data['spTypeAnnoucer']=0
    data['contactPerson'] = PartnerName
    data['bankAccountName'] = '��ͬѧ01'

    #����post����
    r = httputils.postadmin(admin_api, data, admintoken, confutils.getcurrentPath('PartnerEdit'))
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
    add_CopyrightPartner(2)
    add_CopyrightPartner(3)
    add_CopyrightPartner(4)