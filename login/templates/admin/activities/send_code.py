#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/1/17 11:59
# @Author  : caozhuo
# @FileName: send_code.py
# @Software: PyCharm
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/12/24 15:56
# @Author  : caozhuo
# @FileName: lazyviews.py
# @Software: PyCharm
import datetime
import json
import random
from time import sleep

from login.templates.admin.anchor.Anchor_Operation import get_user_info_dict
from login.templates.admin.account.adminlogin import login_admin
from login.templates.utils import httputils, confutils, dbutil
from login.templates.utils.confutils import getAdminName
from login.templates.utils.utils import ranstr, get_local_time_day
from login.templates.config import constant


def send_ticket_by_exchangeCode(ticket_amount: str, user_id: str, use_scope='0'):
    """
    通过兑换码送券给指定用户,支持发特定属性及随机属性
    :param use_scope: 使用范围，【随机属性】默认传0（通用）,具体参考constant.py下的“兑换码使用范围”
                                【特定属性】use_scope传字典，格式为：{'name':'#书籍名','id':'#书籍id','scope':'22'}，scope值参考constant.py下的“兑换码使用范围”
    :param ticket_amount:赠券金额，str,具体参考constant.py下的“兑换码兑换面额”
    :param user_id:待发券的指定用户
    :return:
    """
    # 添加活动【随机属性】
    if isinstance(use_scope, str):
        # 通用使用范围
        if use_scope == '0':
            activity_dict = add_listen_tickets(ticket_amount, {'scope': use_scope})
            print('活动字典信息：',activity_dict)
        # 非通用
        else:
            activity_dict = add_listen_tickets(ticket_amount, get_use_scope_info(use_scope))
    # 兼容【特定属性】
    else:
        activity_dict = add_listen_tickets(ticket_amount, use_scope)
    # 审核
    approve_res = approve_listen_tickets(activity_dict['activityId'])
    if approve_res == 'pass':
        # 获取未兑换的活动code
        code_list = get_activity_CodeList(activity_dict)
        # 绑定code
        band_activity_Code(code_list[0], user_id)
        return 0
    else:
        return '审核不通过，生成失败'


def send_vip_by_exchangeCode(swapGoodsId: str, user_id: str):
    """
    通过兑换码送vip给指定用户
    :param swapGoodsId:兑换值，具体值参考constant.py的"vip的兑换值"
    :param user_id:
    :return:
    """
    # 发起vip申请
    activity_dict = add_vip_exchange_code(swapGoodsId)
    # 审核
    approve_res = approve_listen_tickets(activity_dict['activityId'])
    if approve_res == 'pass':
        # 获取未兑换的活动code
        code_list = get_activity_CodeList(activity_dict)
        # 绑定code
        band_activity_Code(code_list[0], user_id)
        return 1
    else:
        return approve_res


def add_vip_exchange_code(swapGoodsId: str):
    """
    添加vip
    :param swapGoodsId:兑换值，具体值参考constant.py的"vip的兑换值"
    :return:
    """
    orgName = 'AT' + ranstr(6)
    data = {
        'swapGoodsType': '1',
        'isActivityGift': '0',
        'swapGoodsId': swapGoodsId,
        'beginUseTime': get_local_time_day(),
        'givenUserType': '0',
        'orgName': orgName,
        'swapNum': '1',
        'startTime': datetime.date.today(),
        'timeRange': '15',
        'maxForUser': '0:1',
        'detail': 'AT' + ranstr(4)
    }
    r = httputils.postadmin(getAdminName('activityAdd'),
                            data,
                            login_admin(),
                            confutils.getcurrentPath('ActivityAdd'))
    result = json.loads(r.text)
    print(result)
    if result['status'] == 0:
        code_id = dbutil.select('SELECT id  FROM `t_activity` WHERE org_name=\'%s\'' % orgName, 'db_audiobook')
        if code_id:
            return {'activityId': code_id[0]['id'], 'orgName': orgName}
        else:
            return '查无此活动id'
    else:
        return result['msg']


def add_listen_tickets(ticket_amount: str, goods_info: dict):
    """
    添加兑换码赠券
    :param goods_info: 用户使用范围非通用时，需要传的信息，格式如：goods_info={'name':'#书籍名','id':'#书籍id','scope':'22'}
    :param ticket_amount:券面值 str
    :param use_scope:使用范围 str
    :return:
    """
    if ticket_amount == '1':
        swapGoodsId = '121'
    elif ticket_amount == '2':
        swapGoodsId = '122'
    elif ticket_amount == '5':
        swapGoodsId = '123'
    elif ticket_amount == '10':
        swapGoodsId = '124'
    elif ticket_amount == '20':
        swapGoodsId = '125'
    elif ticket_amount == '50':
        swapGoodsId = '126'
    elif ticket_amount == '100':
        swapGoodsId = '127'
    elif ticket_amount == '150':
        swapGoodsId = '150'
    elif ticket_amount == '200':
        swapGoodsId = '151'
    elif ticket_amount == '300':
        swapGoodsId = '152'
    elif ticket_amount == '500':
        swapGoodsId = '153'
    else:
        print('参数错误！')
    orgName = 'AT' + ranstr(6)
    data = {
        'swapGoodsType': '2',
        'isActivityGift': '0',
        'swapGoodsId': swapGoodsId,
        'goodsUseScope': goods_info['scope'],
        'beginUseTime': get_local_time_day(),
        'swapExpireTime': '15',
        'givenUserType': '0',
        'orgName': orgName,
        'swapNum': '2',
        'startTime': datetime.date.today(),
        'timeRange': '15',
        'maxForUser': '0:2',
        'detail': 'AT' + ranstr(4)
    }
    if goods_info['scope'] == '0':
        end_data = data
    else:
        branch_data = {'goods_type_name': goods_info['name'], 'goods_type_id': goods_info['id']}
        end_data = {**data, **branch_data}
    r = httputils.postadmin(getAdminName('activityAdd'),
                            end_data,
                            login_admin(),
                            confutils.getcurrentPath('ActivityAdd'))
    result = json.loads(r.text)
    print(result)
    if result['status'] == 0:
        code_id = dbutil.select('SELECT id  FROM `t_activity` WHERE org_name=\'%s\'' % orgName, 'db_audiobook')
        sleep(0.2)
        if code_id:
            return {'activityId': code_id[0]['id'], 'orgName': orgName}
        else:
            return '查无此活动id'
    else:
        return result['msg']


def approve_listen_tickets(activity_id: str):
    """
    审核兑换码
    :param activity_id:兑换码id，str
    :return:兑换结果
    """
    r = httputils.postadmin(getAdminName('activityApprove'),
                            {'id': activity_id},
                            login_admin(),
                            confutils.getcurrentPath('ActivityList'))
    result = json.loads(r.text)
    if result['status'] == 0:
        return 'pass'
    else:
        return result['msg']


def get_activity_CodeList(data: dict):
    """
    获取兑换码code
    :param data:
    :return:返回未兑换的兑换code
    """
    dict_page = {'pageNum': '1', 'pageSize': '500'}
    r = httputils.postadmin(getAdminName('activityCodeList'),
                            {**data, **dict_page},
                            login_admin(),
                            confutils.getcurrentPath('ActivityCodeList'))
    result = json.loads(r.text)
    print(result)
    res_list = result['list']
    back_list = []
    for code in res_list:
        if code['status'] == 1:
            back_list.append(code['id'])
    return back_list


def band_activity_Code(code_id: str, user_id: str):
    """
    兑换code绑定用户
    :param code_id:str
    :param user_id:str
    :return:
    """
    r = httputils.postadmin(getAdminName('activityCodeBandingAdd'),
                            {'id': code_id,
                             'userId': user_id,
                             'nickName': get_user_info_dict(int(user_id))['nickName'],
                             'reason': 'reason' + ranstr(3)
                             },
                            login_admin(),
                            confutils.getcurrentPath('ActivityCodeList'))
    result = json.loads(r.text)
    print(result)
    if result['status'] == 0:
        return '绑定成功'
    else:
        return result['msg']


def get_use_scope_info(scope_type: str):
    """
    获取兑换码使用范围
    :param scope_type:兑换码类型
    :return:
    """
    # 指定上传者
    if scope_type == constant.exchange_Code_specUploader:
        # cnt = random.randint(0, 9)
        anchor_info = dbutil.select(
            'SELECT user_id,nick_name FROM t_user_ext_%d LIMIT %d,1' % (random.randint(0, 9), random.randint(0, 9)),
            'db_audiobook')
        print(anchor_info)
        return {'name': anchor_info[0]['nick_name'], 'id': anchor_info[0]['user_id'], 'scope': scope_type}
    # 指定阅读版权机构
    elif scope_type == constant.exchange_Code_specRead_copyright:
        partner_info = dbutil.select(
            'SELECT t.`id`,t1.`code_value` FROM t_sns_partner t INNER JOIN t_sns_partner_ext t1 ON '
            't.`id`=t1.`partner_id` AND t1.`code`=\'org_name\'AND t.`type`=11 LIMIT %d,1' % random.randint(0, 9),
            'db_audiobook')
        print(partner_info)
        return {'name': partner_info[0]['code_value'], 'id': partner_info[0]['id'], 'scope': scope_type}
    # 指定阅读分类
    elif scope_type == constant.exchange_Code_Read_Classify:
        type_info = dbutil.select(
            'SELECT t.`type_id`,t.`type_name` FROM t_type t INNER JOIN t_read_book_type t1 ON t.`type_id`=t1.`type_id` LIMIT %d,1' % random.randint(
                0, 9),
            'db_audiobook')
        print(type_info)
        return {'name': type_info[0]['type_name'], 'id': str(type_info[0]['type_id']), 'scope': scope_type}
    # 指定阅读书籍
    elif scope_type == constant.exchange_Code_Read_book:
        type_info = dbutil.select(
            'SELECT id, book_name FROM t_read_book WHERE state=1 LIMIT %d,1' % random.randint(0, 9), 'db_audiobook')
        print(type_info)
        return {'name': type_info[0]['book_name'], 'id': type_info[0]['id'], 'scope': scope_type}
    # 指定听书版权机构
    elif scope_type == constant.exchange_Code_specListen_copyright:
        copyright_info = dbutil.select(
            'SELECT id,copy_name FROM t_copyright LIMIT %d,1' % random.randint(0, 9), 'db_audiobook')
        print(copyright_info)
        return {'name': copyright_info[0]['copy_name'], 'id': copyright_info[0]['id'], 'scope': scope_type}
    # 指定有声听书分类
    elif scope_type == constant.exchange_Code_Listen__Classify:
        type_info = dbutil.select(
            'SELECT type_id,type_name FROM `t_type` where father_type=6000  LIMIT %d,1' % random.randint(0, 9),
            'db_audiobook')
        print(type_info)
        return {'name': type_info[0]['type_name'], 'id': type_info[0]['type_id'], 'scope': scope_type}
    # 指定有声书籍
    elif scope_type == constant.exchange_Code_ListenBook:
        book_info = dbutil.select(
            'SELECT book_id,book_name FROM t_book WHERE bState=0 AND pay_free=1 LIMIT %s,1' % random.randint(0, 9),
            'db_audiobook')
        print(book_info)
        return {'name': book_info[0]['book_name'], 'id': book_info[0]['book_id'], 'scope': scope_type}
    # 指定有声节目
    elif scope_type == constant.exchange_Code_Listen_Albumn:
        albumn_info = dbutil.select(
            'SELECT id,name FROM t_sns_ablumn WHERE STATUS=0 AND pay_free=1 LIMIT %s,1' % random.randint(0, 9),
            'db_audiobook')
        print(albumn_info)
        return {'name': albumn_info[0]['name'], 'id': albumn_info[0]['id'], 'scope': scope_type}
    else:
        return 'scope值或格式错误'
