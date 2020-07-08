# coding=gbk
from login.templates.admin.platform.common.operate_mysql import billing_select

import re


def partnerName(cooperator_type):
    '''生成分成合作方全称
    :param cooperator_type 合作方类型 1=渠道 2=版权 3=主播
    '''
    if cooperator_type == 1:
        partnerName = '渠道合作方'
    elif cooperator_type == 2:
        partnerName = '版权合作方'
    elif cooperator_type == 3:
        partnerName = '主播合作方'
    else:
        print('-------输入错误！！！只能输入1或2或3-------')
    partner_record = billing_select('SELECT * from billing.p_partner ORDER BY id desc LIMIT 1;')
    partner_id = partner_record[0]['id']
    partner_id = str(partner_id)
    partner_id_lenth = len(partner_id)
    if partner_id_lenth < 4:
        partnerName_Number = str(int(partner_id) + 1).zfill(4)
    elif partner_id_lenth == 4 and partner_id != '9999':
        partnerName_Number = str(int(partner_id) + 1)
    elif partner_id_lenth > 4 and partner_id[-4:] != '9999':
        partnerName_Number = str(int(partner_id[-4:]) + 1).zfill(4)
    else:
        partnerName_Number = '0001'
    PartnerFullName = partnerName + partnerName_Number
    print(PartnerFullName)
    return[PartnerFullName,partnerName_Number]

if __name__=='__main__':
    partnerName(3)