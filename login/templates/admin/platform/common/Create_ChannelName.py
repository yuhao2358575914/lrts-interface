# coding=gbk
from login.templates.admin.platform.common.operate_mysql import select, readbook_select, billing_select
import re


def releaseChannelName():
    '''生成发布渠道的简称和全称'''
    channel_record = billing_select("select * from platform.t_copyright_channel order by id desc limit 1;")
    channel_id = channel_record[0]['id']
    channel_id = str(channel_id)
    print(channel_id)
    cp_id_lenth = len(channel_id)
    if cp_id_lenth < 4:
        ChannelName_Number = str(int(channel_id) + 1).zfill(4)
    elif cp_id_lenth == 4 and channel_id != '9999':
        ChannelName_Number = str(int(channel_id) + 1)
    elif cp_id_lenth > 4 and channel_id[-4:] != '9999':
        ChannelName_Number = str(int(channel_id[-4:]) + 1).zfill(4)
    else:
        ChannelName_Number = '0001'
    ChannelName = '百度' + ChannelName_Number
    ChannelCode = 'baidu'+ChannelName_Number
    print('发布渠道的名称为：'+ChannelName+'|'+'渠道的代号为：'+ChannelCode)
    return [ChannelName,ChannelCode]
def divideChannelName():
    '''生成分成渠道的名称'''
    channel_record = billing_select("select * from billing.p_share_fee_channel order by id desc limit 1;")
    channel_id = channel_record[0]['id']
    channel_id = str(channel_id)
    print(channel_id)
    cp_id_lenth = len(channel_id)
    if cp_id_lenth < 4:
        ChannelName_Number = str(int(channel_id) + 1).zfill(4)
    elif cp_id_lenth == 4 and channel_id != '9999':
        ChannelName_Number = str(int(channel_id) + 1)
    elif cp_id_lenth > 4 and channel_id[-4:] != '9999':
        ChannelName_Number = str(int(channel_id[-4:]) + 1).zfill(4)
    else:
        ChannelName_Number = '0001'
    ChannelNickName = '百度渠道' + ChannelName_Number
    ChannelFullName = '百度分成渠道' + ChannelName_Number
    print('分成渠道的简称为:'+ChannelNickName + '|' + '分成渠道的全称为:'+ChannelFullName)
    return [ChannelNickName, ChannelFullName]
if __name__=='__main__':
    # releaseChannelName()
    divideChannelName()