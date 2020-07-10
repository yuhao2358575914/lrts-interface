# coding=gbk
from login.templates.admin.platform.common.operate_mysql import select, readbook_select, platform_select
import re


def bookName():
    '''生成付费收听版权方全称'''
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
    FullName = '有声书籍版权' + Name_Number
    CopyName = '有声版权' + Name_Number
    print('全称为：' + FullName + '|' + '简称为：' + CopyName)
    return [FullName, CopyName]


def readBookName():
    '''生成电子阅读版权方全称'''
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
    OrgName = '懒人听书' + Name_Number
    FullName = '电子阅读版权' + Name_Number
    CopyName = '阅读版权' + Name_Number
    print('机构名称为：' + OrgName + '|' + '全称为：' + FullName + '|' + '简称为：' + CopyName)
    return [OrgName, FullName, CopyName]


def comicName():
    '''生成漫画版权全称'''
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
    FullName = '漫画版权方' + Name_Number
    ShortName = '漫画版权' + Name_Number
    Contacter = '漫画' + Name_Number
    print('全称为：' + FullName + '|' + '简称为：' + ShortName + '|' + '联系人为：' + Contacter)
    return [FullName, ShortName, Contacter]
