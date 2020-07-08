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
    '''添加播音'''
    admintoken = login_admin()# 登录admin获取token
    admin_api = getAdminName('copyrightAnnouncerEdit')# 获取copyrightEdit接口
    print(admin_api)
    announcerName = Create_AnnouncerName.announcerName() #生成播音名称
    # 入参
    json_data={}
    json_data['announcerName']=announcerName
    json_data['lrBindType']=2
    json_data['yyBindType']=2
    json_data['status']=1
    json_data['lrAnnouncerIds']= ''
    json_data['yyAnnouncerIds']= ''
    json_data['bankInfoList'] = []
    # 发送post请求
    print(confutils.getcurrentPath('announcerEdit'))
    r = httputils.postadmin(admin_api, json_data, admintoken, confutils.getcurrentPath('announcerEdit'))
    if json.loads(r.text)['status']==0:
        Announcer_record = platform_select("select * from platform.t_copyright_announcer order by id desc limit 1;") #查询添加后的版权记录
        Announcer_id=Announcer_record[0]['id'] #获取版权id
        Announcer_name=Announcer_record[0]['name'] #获取版权全称
        print('----------',Announcer_name,'(id为',Announcer_id,')','添加成功！---------')
        return [Announcer_id, Announcer_name]
    else:
        print('---------添加失败!!!-----------')


if __name__=='__main__':
    # add_AudioBookCopyright()
    # add_ReadBookCopyright()
    add_Announcer()
