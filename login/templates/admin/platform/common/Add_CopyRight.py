# coding=gbk
from time import sleep

from login.templates.admin.account.adminlogin import login_admin
from login.templates.admin.platform.common import Create_CopyrightName
from login.templates.admin.platform.common.operate_mysql import billing_select, select
from login.templates.utils import httputils, confutils
from login.templates.utils.confutils import getAdminName
import json


def add_AudioBookCopyright():
    '''��������鼮��Ȩ'''
    admintoken = login_admin()# ��¼admin��ȡtoken
    admin_api = getAdminName('copyrightEdit')# ��ȡcopyrightEdit�ӿ�
    print(admin_api)
    bookNameInfo=Create_CopyrightName.bookName()
    fullName = bookNameInfo[0]  # ���������鼮�İ�Ȩ��ȫ��
    copyName=bookNameInfo[1]  #���������鼮�İ�Ȩ�����

    # ���
    json_data={
        "copyright": {
            "audioCopyrightType": 0,
            "type": 1,
            "copyName":copyName ,
            "fullName":fullName,
            "homePage": "",
            "copyDesc": "",
            "userName": "��ͬѧ001",
            "phone": "15879791234",
            "qq": "",
            "email": "",
            "orgId": ""
        }
    }
    # ����post����
    print(confutils.getcurrentPath('copyrightList'))
    r = httputils.postadmin(admin_api, json_data, admintoken, confutils.getcurrentPath('copyrightList'))
    if json.loads(r.text)['status']==0:
        cp_record = billing_select("select id,full_name from platform.t_copyright WHERE full_name like'%��Ȩ%' order by id desc limit 1;","platform") #��ѯ��Ӻ�İ�Ȩ��¼
        cp_id=cp_record[0]['id'] #��ȡ��Ȩid
        cp_name=cp_record[0]['full_name'] #��ȡ��Ȩȫ��
        print('----------',cp_name,'(idΪ',cp_id,')','��ӳɹ���---------')
        return [cp_id, cp_name]
    else:
        print('---------���ʧ��!!!-----------')

def add_ReadBookCopyright():
    '''��ӵ����Ķ���Ȩ��'''
    admintoken = login_admin()  # ��¼admin��ȡtoken
    admin_api=getAdminName('orgUpdate')
    readBookNameInfo=Create_CopyrightName.readBookName()
    orgName = readBookNameInfo[0] #���ɵ����Ķ���������
    fullName = readBookNameInfo[1]  # ���ɵ����Ķ��İ�Ȩ��ȫ��
    copyName = readBookNameInfo[2] #���ɵ����Ķ��İ�Ȩ�����
    data={'id':'',
          'qq':'',
          'webSite':'',
          'link':'',
          'postalAddress':'',
          'email':'',
          'description':'',
          'cover':'',
          'rename':'',
          'file':'',
          }
    data['orgName']=orgName
    data['fullName']=fullName
    data['copyName']=copyName
    data['typeId']=5001
    data['realName']='��ͬѧ001'
    data['phone']='15879791236'
    data['orgType']=11
    # ����post����
    print(confutils.getcurrentPath('ReadOrgEdit'))
    r = httputils.postadmin(admin_api, data, admintoken, confutils.getcurrentPath('ReadOrgEdit'))
    if json.loads(r.text)['status'] == 0:
        cp_record = billing_select("select * from readbook.rb_partner_ext WHERE code='org_name' and code_value like'��������%' order by partner_id desc limit 1;","readbook")  # ��ѯ��Ӻ�İ�Ȩ��¼
        sleep(3)
        cp_id = cp_record[0]['partner_id']  # ��ȡ��Ȩid
        print(cp_id)
        org_name = cp_record[0]['code_value']  # ��ȡ��Ȩȫ��
        print(org_name)
        print('----------', org_name, '(idΪ', cp_id, ')', '��ӳɹ���---------')
        return [cp_id, org_name]
    else:
        print('---------���ʧ��!!!-----------')
def add_ComicCopyright():
    '''���������Ȩ��'''
    admintoken = login_admin()  # ��¼admin��ȡtoken
    admin_api = getAdminName('copyright_edit')
    comicNameInfo=Create_CopyrightName.comicName()
    fullName = comicNameInfo[0]  # ���������İ�Ȩ��ȫ��
    shortName =comicNameInfo[1]  # ���������İ�Ȩ�����
    contacter =comicNameInfo[2] #������������ϵ��
    data={}
    data['fullName'] = fullName
    data['shortName'] = shortName
    data['contacter'] = contacter
    data['phone'] = 15879791231
    data['remark'] = '�Զ����������'
    # ����post����
    print(confutils.getcurrentPath('ComicEdit'))
    r = httputils.postadmin(admin_api, data, admintoken, confutils.getcurrentPath('ComicEdit'))
    if json.loads(r.text)['status'] == 0:
        cp_record = select("select * from yyting_partdb.c_comic_copyright  order by id desc limit 1;","yyting_partdb")  # ��ѯ��Ӻ�İ�Ȩ��¼
        cp_id = cp_record[0]['id']  # ��ȡ��Ȩid
        print(cp_id)
        full_name = cp_record[0]['full_name']  # ��ȡ��Ȩȫ��
        print(full_name)
        print('----------', full_name, '(idΪ', cp_id, ')', '��ӳɹ���---------')
        return [cp_id, full_name]
    else:
        print('---------���ʧ��!!!-----------')
if __name__=='__main__':
    add_AudioBookCopyright()
    # add_ReadBookCopyright()
    # add_ComicCopyright()