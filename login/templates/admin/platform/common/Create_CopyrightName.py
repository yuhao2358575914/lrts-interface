# coding=gbk
from login.templates.admin.platform.common.operate_mysql import select, readbook_select, platform_select
import re


def bookName():
    '''���ɸ���������Ȩ��ȫ��'''
    cp_record = platform_select("select * from platform.t_copyright  order by id desc limit 1;")
    cp_id = cp_record[0]['id']
    cp_id = str(cp_id)
    cp_id_lenth = len(cp_id)
    if cp_id_lenth < 4:
        Name_Number = str(int(cp_id) + 1).zfill(4)
    elif cp_id_lenth == 4 and cp_id != '9999':
        Name_Number = str(int(cp_id) + 1)
    elif cp_id_lenth > 4 and cp_id[-4:] != '9999':
        Name_Number = str(int(cp_id[-4:]) + 1).zfill(4)
    else:
        Name_Number = '0001'
    FullName = '�����鼮��Ȩ' + Name_Number
    CopyName = '������Ȩ' + Name_Number
    print('ȫ��Ϊ��' + FullName + '|' + '���Ϊ��' + CopyName)
    return [FullName, CopyName]


def readBookName():
    '''���ɵ����Ķ���Ȩ��ȫ��'''
    cp_record = readbook_select("select * from readbook.rb_partner_ext order by partner_id desc limit 1;")
    cp_id = cp_record[0]['partner_id']
    cp_id = str(cp_id)
    cp_id_lenth = len(cp_id)
    if cp_id_lenth < 4:
        Name_Number = str(int(cp_id) + 1).zfill(4)
    elif cp_id_lenth == 4 and cp_id != '9999':
        Name_Number = str(int(cp_id) + 1)
    elif cp_id_lenth > 4 and cp_id[-4:] != '9999':
        Name_Number = str(int(cp_id[-4:]) + 1).zfill(4)
    else:
        Name_Number = '0001'
    OrgName = '��������' + Name_Number
    FullName = '�����Ķ���Ȩ' + Name_Number
    CopyName = '�Ķ���Ȩ' + Name_Number
    print('��������Ϊ��' + OrgName + '|' + 'ȫ��Ϊ��' + FullName + '|' + '���Ϊ��' + CopyName)
    return [OrgName, FullName, CopyName]


def comicName():
    '''����������Ȩȫ��'''
    cp_record = select("select * from yyting_partdb.c_comic_copyright order by id desc limit 1;", "yyting_partdb")
    cp_id = cp_record[0]['id']
    cp_id = str(cp_id)
    print(cp_id)
    cp_id_lenth = len(cp_id)
    if cp_id_lenth < 4:
        Name_Number = str(int(cp_id) + 1).zfill(4)
    elif cp_id_lenth == 4 and cp_id != '9999':
        Name_Number = str(int(cp_id) + 1)
    elif cp_id_lenth > 4 and cp_id[-4:] != '9999':
        Name_Number = str(int(cp_id[-4:]) + 1).zfill(4)
    else:
        Name_Number = '0001'
    FullName = '������Ȩ��' + Name_Number
    ShortName = '������Ȩ' + Name_Number
    Contacter = '����' + Name_Number
    print('ȫ��Ϊ��' + FullName + '|' + '���Ϊ��' + ShortName + '|' + '��ϵ��Ϊ��' + Contacter)
    return [FullName, ShortName, Contacter]
