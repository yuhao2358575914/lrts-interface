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
    '''�������������
    :param business 0��ʾ��ѡȫ��ҵ�� 1��ʾ�������� 2 ��ʾ�����Ķ� 3 ��ʾ�������� 4��ʾVIP��Ա 5��ʾ����
    :param partnerType 1��ʾ�����˻� 2��ʾ��˾�˻�
    '''
    admintoken = login_admin()  # ��¼admin��ȡtoken
    admin_api = getAdminName('partnerEdit')  # ��ȡpartnerEdit�ӿ�
    print(admin_api)
    # ����׼��
    data = {}
    channelInfo = add_DivideChannel()  # ��ȡ������Ϣ
    channel_id = channelInfo[0]  # ��ȡ����id
    channel_name = channelInfo[1]  # ��ȡ����name
    # channel_id = 5039  # ��ȡ����id
    # channel_name = 'IOS��������'  # ��ȡ����name
    PartnerName_Record = partnerName(1)  # ��������������
    PartnerName = PartnerName_Record[0]  # ����һ���µ���������������
    PartnerName_Number = PartnerName_Record[1]  # ��ȡ�µİ�Ȩ���������ƺ��������
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
        print('���δ������������룡����')
    # �ӿ����
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
    data['loginName'] = 'zhoushichuanCh' + str(PartnerName_Number)
    data['password'] = 123456
    data['passwordConfirm'] = 123456
    data['partnerType'] = partnerType  # 1��ʾ�����˻� 2��ʾ��˾�˻�
    data['cooperatorType'] = 1  # 1���� 2��Ȩ 3����
    data['bankAccountName'] = '��ͬѧ01'

    # ����post����
    r = httputils.postadmin(admin_api, data, admintoken, confutils.getcurrentPath('PartnerEdit'))
    res = json.loads(r.text)
    print(res)
    if res['status'] == 0:
        Channel_partner = billing_select("SELECT * from billing.p_partner order by id desc LIMIT 1;", "billing")
        Channel_partnerId = Channel_partner[0]['id']
        Channel_partnerName = Channel_partner[0]['full_name']
        print('-----------������������' + Channel_partnerName + '(id:' + str(
            Channel_partnerId) + ')' + '��ӳɹ�������---------------------')
        return [Channel_partnerId, Channel_partnerName]
    else:
        print('---------���ʧ�ܣ�����-----------')


def check_information(business, partnerType):
    '''�ֳɺ������������
    :param business 0��ʾ��ѡȫ��ҵ�� 1��ʾ�������� 2 ��ʾ�����Ķ� 3 ��ʾ�������� 4��ʾVIP��Ա 5��ʾ����
    '''
    admintoken = login_admin()
    admin_api = getAdminName('partnerConfirmEdit')  # ��ȡ�ӿ�
    # ���
    Anchor_partner = add_ChannelPartner(business, partnerType)  # ��ȡ����������id������
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
