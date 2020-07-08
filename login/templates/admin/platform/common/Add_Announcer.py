# coding=gbk
from time import sleep

from login.templates.admin.account.adminlogin import login_admin
from login.templates.admin.platform.common.Create_PartnerName import partnerName
from login.templates.admin.platform.common.operate_mysql import billing_select, select, readbook_select,  \
    platform_select
from login.templates.admin.platform.common import Create_AnnouncerName
from login.templates.utils import httputils, confutils
from login.templates.utils.confutils import getAdminName
import json


def add_Announcer():
    '''��Ӳ���'''
    admintoken = login_admin()# ��¼admin��ȡtoken
    admin_api = getAdminName('copyrightAnnouncerEdit')# ��ȡcopyrightEdit�ӿ�
    print(admin_api)
    announcerName = Create_AnnouncerName.announcerName() #���ɲ�������
    # ���
    json_data={}
    json_data['announcerName']=announcerName
    json_data['lrBindType']=2
    json_data['yyBindType']=2
    json_data['status']=1
    json_data['lrAnnouncerIds']= ''
    json_data['yyAnnouncerIds']= ''
    json_data['bankInfoList'] = []
    # ����post����
    print(confutils.getcurrentPath('announcerEdit'))
    r = httputils.postadmin(admin_api, json_data, admintoken, confutils.getcurrentPath('announcerEdit'))
    if json.loads(r.text)['status']==0:
        Announcer_record = platform_select("select * from platform.t_copyright_announcer order by id desc limit 1;") #��ѯ��Ӻ�İ�Ȩ��¼
        Announcer_id=Announcer_record[0]['id'] #��ȡ��Ȩid
        Announcer_name=Announcer_record[0]['name'] #��ȡ��Ȩȫ��
        print('----------',Announcer_name,'(idΪ',Announcer_id,')','��ӳɹ���---------')
        return [Announcer_id, Announcer_name]
    else:
        print('---------���ʧ��!!!-----------')


if __name__=='__main__':
    # add_AudioBookCopyright()
    # add_ReadBookCopyright()
    add_Announcer()
