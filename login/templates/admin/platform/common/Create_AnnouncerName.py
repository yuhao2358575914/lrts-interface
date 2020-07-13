# coding=gbk
from login.templates.admin.platform.common.operate_mysql import select,billing_select
import re

def announcerName():
    '''生成播音名称'''
    cp_record = billing_select("select * from platform.t_copyright_announcer order by id desc limit 1;","platform")
    cp_id = cp_record[0]['id']
    cp_id = str(cp_id)
    cp_id_lenth = len(cp_id)
    if cp_id_lenth < 4:
        AnnouncerName_Number = str(int(cp_id) + 1).zfill(4)
    elif cp_id_lenth == 4 and cp_id != '9999':
        AnnouncerName_Number = str(int(cp_id) + 1)
    elif cp_id_lenth > 4 and cp_id[-4:] != '9999':
        AnnouncerName_Number = str(int(cp_id[-4:]) + 1).zfill(4)
    else:
        AnnouncerName_Number = '0001'
    AnnouncerName = '播音' + AnnouncerName_Number
    print('播音的名称为：'+AnnouncerName)
    return AnnouncerName

if __name__=='__main__':
    announcerName()
