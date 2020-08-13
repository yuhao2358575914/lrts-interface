# coding=gbk
import random

from login.templates.admin.account.adminlogin import login_admin

from login.templates.admin.platform.common.Add_Announcer import add_Announcer
from login.templates.admin.platform.common.Create_PartnerName import partnerName
from login.templates.admin.platform.common.Create_Number import create_PhoneNum, create_IDNumber, \
    create_CreditCardNumbers
from login.templates.admin.platform.common.operate_mysql import billing_select, select
from login.templates.utils import httputils, confutils
from login.templates.utils.confutils import getAdminName
import json

from login.templates.utils.httputils import getadmin


def add_AnchorPartner(business, partnerType):
    '''�������������
    :param business 0��ѡȫ��ҵ�� 1��ʾ�������� 2 ��ʾ�������� 3 ��ʾVIP��Ա
    :param partnerType 1��ʾ�����˻� 2��ʾ��˾�˻�
    '''
    admintoken = login_admin()  # ��¼admin��ȡtoken
    admin_api = getAdminName('partnerEdit')  # ��ȡpartnerEdit�ӿ�
    print(admin_api)
    # ����׼��
    data = {}
    book_cp = add_Announcer()  # ��ȡ������Ϣ
    book_cp_id = book_cp[0]  # ��ȡ����id
    book_cp_name = book_cp[1]  # ��ȡ����name
    PartnerName_Record = partnerName(3)  # ��������������
    PartnerName = PartnerName_Record[0]  # ����һ���µ���������������
    PartnerName_Number = PartnerName_Record[1]  # ��ȡ�µ��������������ƺ��������
    # �ж��Ǹ����˻����ǹ�˾�˻�
    if partnerType == 1:
        data['contactPerson'] = PartnerName + '(�����˻�)'
    elif partnerType == 2:
        data['fullName'] = PartnerName + '(��˾�˻�)'
        data['shortName'] = PartnerName + '(��˾�˻�)'
        data['contactPerson'] = PartnerName + '(��˾�˻�)'
        data['deductTaxRate'] = random.randint(2, 20)
    else:
        print('�˻������������󣡣���')
    if business == 0:
        data['spTypeBook'] = 1
        data['spTypeReadBook'] = 0
        data['spTypeVIP'] = 1
        data['spTypeComic'] = 0
        data['spTypeAnnoucer'] = 1
        data['annoucerEntityId'] = book_cp_id
        data['annoucerEntityName'] = book_cp_name
    elif business == 1:
        data['spTypeBook'] = 1
        data['spTypeReadBook'] = 0
        data['spTypeVIP'] = 0
        data['spTypeComic'] = 0
        data['spTypeAnnoucer'] = 0
        data['annoucerEntityId'] = book_cp_id
        data['annoucerEntityName'] = book_cp_name
    elif business == 2:
        data['spTypeBook'] = 0
        data['spTypeReadBook'] = 0
        data['spTypeVIP'] = 0
        data['spTypeComic'] = 0
        data['spTypeAnnoucer'] = 1
        data['annoucerEntityId'] = book_cp_id
        data['annoucerEntityName'] = book_cp_name
    elif business == 3:
        data['spTypeBook'] = 0
        data['spTypeReadBook'] = 0
        data['spTypeVIP'] = 1
        data['spTypeComic'] = 0
        data['spTypeAnnoucer'] = 0
        data['annoucerEntityId'] = book_cp_id
        data['annoucerEntityName'] = book_cp_name
    else:
        print('���δ������������룡����')
    # �ӿ����
    data['id'] = ''
    data['bookEntityId'] = ''
    data['bookEntityName'] = ''
    data['readbookEntityId'] = ''
    data['readbookEntityName'] = ''
    data['comicEntityId'] = ''
    data['comicEntityName'] = ''
    data['channelEntityId'] = ''
    data['channelEntityName'] = ''
    data['partnerStatus'] = 2
    data['canLogin'] = 0
    data['contactPerson'] = PartnerName
    data['identityCode'] = create_IDNumber()
    data['phone'] = create_PhoneNum()
    data['qq'] = ''
    data['email'] = ''
    data['address'] = '��������ɽ�������ֵ�'
    data['postcode'] = ''
    data['bankAccount'] = create_CreditCardNumbers()
    data['bankType'] = 1  # 1��ʾ�й�����
    data['bankProvince'] = 17
    data['bankCity'] = 285
    data['bankName'] = '�������й�������ɽ����'
    data['taxType'] = 0
    data['billType'] = 1
    data['billCode'] = ''
    data['buttMan'] = ''
    data['loginName'] = 'zhoushichuanAnch' + str(PartnerName_Number)
    data['password'] = 123456
    data['passwordConfirm'] = 123456
    data['partnerType'] = partnerType  # 1��ʾ�����˻� 2��ʾ��˾�˻�
    data['cooperatorType'] = 3  # 1���� 2��Ȩ 3����
    data['bankAccountName'] = '��ͬѧ01'

    # ����post����
    r = httputils.postadmin(admin_api, data, admintoken, confutils.getcurrentPath('PartnerEdit'))
    res = json.loads(r.text)
    print(res)
    if res['status'] == 0:
        Anchor_partner = billing_select("SELECT * from billing.p_partner order by id desc LIMIT 1;", "billing")
        Anchor_partnerId = Anchor_partner[0]['id']
        Anchor_partnerName = Anchor_partner[0]['full_name']
        print('-----------������������' + Anchor_partnerName + '(id:' + str(
            Anchor_partnerId) + ')' + '��ӳɹ�������---------------------')
        return [Anchor_partnerId, Anchor_partnerName]
    else:
        print('---------���ʧ�ܣ�����-----------')


def check_information(business, partnerType):
    '''�ֳɺ������������
    :param business 1��ʾ�������� 2 ��ʾ�������� 3 ��ʾVIP��Ա
    '''
    admintoken = login_admin()
    admin_api = getAdminName('partnerConfirmEdit')  # ��ȡ�ӿ�
    # ���
    Anchor_partner = add_AnchorPartner(business, partnerType)  # ��ȡ����������id������
    Anchor_partnerId = Anchor_partner[0]  # ��ȡ����������id
    Anchor_partnerName = Anchor_partner[1]  # ��ȡ��������������
    data = {}
    data['id'] = str(Anchor_partnerId)
    data['partnerStatus'] = '0'
    # ����get����
    res = getadmin(admin_api, data, admintoken, confutils.getcurrentPath('PartnerList'))
    r = json.loads(res.text)
    print(r)
    if r['status'] == 0:
        print('--------������������' + Anchor_partnerName + '(id:' + str(Anchor_partnerId) + ')' + '��Դ���ͨ������-----------')
    else:
        print('--------������������Դ���ʧ�ܣ���-----------')

if __name__=='__main__':
    add_AnchorPartner(1,2)