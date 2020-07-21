# 登录admin获取token
import json
from time import sleep

from login.templates.admin.account.adminlogin import login_admin
from login.templates.admin.common.utilstool import auto_gen_channelID, auto_gen_referID
from login.templates.utils import httputils, confutils, dbutil
from login.templates.utils.confutils import getAdminName
from login.templates.utils.utils import ranstr, get_local_time_day


def add_channel_by_type(channel_type: str):
    """
    添加开发者渠道
    :param channel_type:渠道类型：2-拉取，3-推送
    :return:渠道信息
    """
    admintoken = login_admin()
    chanel_name = "AutoAdd" + ranstr(10)
    # 请求入参
    data = {
        'id': '',
        'type': channel_type,
        'nickName': chanel_name,
        'fullName': chanel_name,
        'referChannelId': str(auto_gen_channelID()),
        'referChannelName': chanel_name,
        'referKey': auto_gen_referID(),
        'channelStatus': '2',
        'startTime': get_local_time_day(),
        'endTime': get_local_time_day(2),
        'protocolType': '0',
        'encryptType': '0',
        'website': '',
        'description': '',
        'contactId': '',
        'contactName': '',
        'contactPhone': '',
        'contactQq': '',
        'contactEmail': '',
        'contactAddress': '',
        'partnerInfoId': '',
        'contractNo': '',
        'bookCount': '',
        'cooperationInfo': '',
        'ipWhiteList': ''
    }

    r = httputils.postadmin(getAdminName('openChannelEdit'),
                            data,
                            admintoken,
                            confutils.getcurrentPath('OpenChannelEdit'))
    print(r.text)
    if json.loads(r.text)['status'] == 0:
        res = dbutil.select('SELECT id,nick_name FROM `p_share_fee_channel` WHERE full_name= "%s"' % chanel_name,
                            'db_audiobook')
        sleep(0.1)
        return res[0]
    else:
        return json.loads(r.text)['msg']


def get_channel_info(chanel_id: str):
    """
    获取渠道信息
    :param chanel_id:渠道id
    :return:
    """
    admintoken = login_admin()
    # 请求入参
    data = {
        'channelId': chanel_id
    }

    r = httputils.postadmin(getAdminName('openChannelGet'),
                            data,
                            admintoken,
                            confutils.getcurrentPath('OpenChannelEdit'))
    print(r.text)
    if json.loads(r.text)['status'] == 0:
        return json.loads(r.text)['channel']
    else:
        return json.loads(r.text)['msg']


def approve_channel_by_id(channel_id: str):
    """
    审核渠道
    :param channel_id:渠道id
    :return:
    """
    # 获取待审渠道信息
    channel_info = get_channel_info(channel_id)
    print('获取的信息', channel_info)
    data = {'id': str(channel_info['id']), 'type': str(channel_info['type']), 'nickName': channel_info['nickName'],
            'fullName': channel_info['fullName'], 'referChannelId': channel_info['referChannelId'],
            'referChannelName': channel_info['referChannelName'], 'referKey': channel_info['referKey'],
            'channelStatus': '1', 'website': channel_info['website'], 'description': channel_info['description'],
            'contactId': channel_info['contactId'], 'contactName': channel_info['contactName'],
            'contactPhone': channel_info['contactPhone'], 'contactQq': channel_info['contactQq'],
            'contactEmail': channel_info['contactEmail'], 'contactAddress': channel_info['contactAddress'],
            'partnerInfoId': channel_info['partnerInfoId'], 'contractNo': channel_info['contractNo'],
            'bookCount': channel_info['bookCount'], 'startTime': channel_info['startTime'],
            'endTime': channel_info['endTime'], 'cooperationInfo': channel_info['cooperationInfo'],
            'protocolType': channel_info['protocolType'], 'ipWhiteList': channel_info['ipWhiteList'],
            'encryptType': channel_info['encryptType']}
    r = httputils.postadmin(getAdminName('openChannelEdit'),
                            data,
                            login_admin(),
                            confutils.getcurrentPath('OpenChannelEdit'))
    print(r.text)
    if json.loads(r.text)['status'] == 0:
        res = dbutil.select(
            'SELECT id,nick_name FROM `p_share_fee_channel` WHERE full_name= "%s"' % channel_info['fullName'],
            'db_audiobook')
        sleep(0.1)
        return res[0]
    else:
        return json.loads(r.text)['msg']
