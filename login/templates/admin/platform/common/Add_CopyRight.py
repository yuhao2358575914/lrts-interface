# coding=gbk
from time import sleep

from login.templates.admin.account.adminlogin import login_admin
from login.templates.admin.platform.common import Create_CopyrightName
from login.templates.admin.platform.common.operate_mysql import billing_select, select
from login.templates.utils import httputils, confutils
from login.templates.utils.confutils import getAdminName
import json


def add_AudioBookCopyright():
    '''添加有声书籍版权'''
    admintoken = login_admin()# 登录admin获取token
    admin_api = getAdminName('copyrightEdit')# 获取copyrightEdit接口
    print(admin_api)
    bookNameInfo=Create_CopyrightName.bookName()
    fullName = bookNameInfo[0]  # 生成有声书籍的版权方全称
    copyName=bookNameInfo[1]  #生成有声书籍的版权方简称

    # 入参
    json_data={
        "copyright": {
            "audioCopyrightType": 0,
            "type": 1,
            "copyName":copyName ,
            "fullName":fullName,
            "homePage": "",
            "copyDesc": "",
            "userName": "周同学001",
            "phone": "15879791234",
            "qq": "",
            "email": "",
            "orgId": ""
        }
    }
    # 发送post请求
    print(confutils.getcurrentPath('copyrightList'))
    r = httputils.postadmin(admin_api, json_data, admintoken, confutils.getcurrentPath('copyrightList'))
    if json.loads(r.text)['status']==0:
        cp_record = billing_select("select id,full_name from platform.t_copyright WHERE full_name like'%版权%' order by id desc limit 1;","platform") #查询添加后的版权记录
        cp_id=cp_record[0]['id'] #获取版权id
        cp_name=cp_record[0]['full_name'] #获取版权全称
        print('----------',cp_name,'(id为',cp_id,')','添加成功！---------')
        return [cp_id, cp_name]
    else:
        print('---------添加失败!!!-----------')

def add_ReadBookCopyright():
    '''添加电子阅读版权方'''
    admintoken = login_admin()  # 登录admin获取token
    admin_api=getAdminName('orgUpdate')
    readBookNameInfo=Create_CopyrightName.readBookName()
    orgName = readBookNameInfo[0] #生成电子阅读机构名称
    fullName = readBookNameInfo[1]  # 生成电子阅读的版权方全称
    copyName = readBookNameInfo[2] #生成电子阅读的版权方简称
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
    data['realName']='周同学001'
    data['phone']='15879791236'
    data['orgType']=11
    # 发送post请求
    print(confutils.getcurrentPath('ReadOrgEdit'))
    r = httputils.postadmin(admin_api, data, admintoken, confutils.getcurrentPath('ReadOrgEdit'))
    if json.loads(r.text)['status'] == 0:
        cp_record = billing_select("select * from readbook.rb_partner_ext WHERE code='org_name' and code_value like'懒人听书%' order by partner_id desc limit 1;","readbook")  # 查询添加后的版权记录
        sleep(3)
        cp_id = cp_record[0]['partner_id']  # 获取版权id
        print(cp_id)
        org_name = cp_record[0]['code_value']  # 获取版权全称
        print(org_name)
        print('----------', org_name, '(id为', cp_id, ')', '添加成功！---------')
        return [cp_id, org_name]
    else:
        print('---------添加失败!!!-----------')
def add_ComicCopyright():
    '''添加漫画版权方'''
    admintoken = login_admin()  # 登录admin获取token
    admin_api = getAdminName('copyright_edit')
    comicNameInfo=Create_CopyrightName.comicName()
    fullName = comicNameInfo[0]  # 生成漫画的版权方全称
    shortName =comicNameInfo[1]  # 生成漫画的版权方简称
    contacter =comicNameInfo[2] #生成漫画的联系人
    data={}
    data['fullName'] = fullName
    data['shortName'] = shortName
    data['contacter'] = contacter
    data['phone'] = 15879791231
    data['remark'] = '自动化测试添加'
    # 发送post请求
    print(confutils.getcurrentPath('ComicEdit'))
    r = httputils.postadmin(admin_api, data, admintoken, confutils.getcurrentPath('ComicEdit'))
    if json.loads(r.text)['status'] == 0:
        cp_record = select("select * from yyting_partdb.c_comic_copyright  order by id desc limit 1;","yyting_partdb")  # 查询添加后的版权记录
        cp_id = cp_record[0]['id']  # 获取版权id
        print(cp_id)
        full_name = cp_record[0]['full_name']  # 获取版权全称
        print(full_name)
        print('----------', full_name, '(id为', cp_id, ')', '添加成功！---------')
        return [cp_id, full_name]
    else:
        print('---------添加失败!!!-----------')
if __name__=='__main__':
    add_AudioBookCopyright()
    # add_ReadBookCopyright()
    # add_ComicCopyright()