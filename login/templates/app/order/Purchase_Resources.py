import json
import uuid
from login.templates.admin.account.user_account import charge_coin_to_user
from login.templates.app.account.Account_Recharge import get_user_account_amount
from login.templates.app.account.Get_Logon_Token import get_app_login_token
from login.templates.app.order.Entity_Price import get_entity_price_by_id, get_entity_price_totalFee
from login.templates.config import constant
from login.templates.users.Get_UserInfo_By_Token import get_ticketBalance_by_token, get_userid_by_token
from login.templates.utils import getconf, httputils, dbutil
from login.templates.utils.confutils import getApiName


def init_uuid():
    """
    生成UUID
    :return:
    """
    return str(uuid.uuid1())  # 根据 时间戳生成 uuid , 保证全球唯一


def geturl_haslist(parameters):
    """
    入参含有list时url拼接
    :param parameters:
    :return:
    """
    keys = []
    for k, v in parameters.items():
        keys.append(k)
    keys.sort(reverse=False)
    url = ''
    for key in keys:
        url = url + key + "=" + parameters[key] + "&"
    return url.rstrip('&')


def buy_book_utils(token, bookid: str, items: list, opType: str, ptype: str, useTicketsType: str, useTickets=''):
    """
    购买书籍
    :param token:
    :param useTickets:
    :return:
    :param useTicketsType:用券类型：0.默认 1.用户选择听读券 2.不使用听读券
    :param bookid:书籍id
    :param items:书籍章节
    :param opType:Item模式
    :param ptype:购买方式，来自于constant文件
    :return:orderNo，类型为str
    """
    # 登录获取token
    # token = get_app_login_token()
    # 获取资源价格信息
    dict_res = get_entity_price_by_id(bookid, constant.resourceType_book)
    # 获取outOrderNo
    outOrderNo = init_uuid()
    # 获取听读券余额
    ticks = get_ticketBalance_by_token(token)
    # 获取账户余额,不够钱自动充值
    headers = getconf.getdict('Headers', 'user-agent')
    if 'Android' in headers.get('user-agent'):
        balance = get_user_account_amount(token, constant.coinType_Andriod)
        if float(balance) + float(ticks) < float(dict_res.get('price')):
            charge_coin_to_user(constant.coinType_Andriod, dict_res.get('price'), get_userid_by_token(token))
    elif 'iOS' in headers.get('user-agent'):
        balance = get_user_account_amount(token, constant.coinType_ios)
        if float(balance) + float(ticks) < float(dict_res.get('price')):
            charge_coin_to_user(constant.coinType_ios, dict_res.get('price'), get_userid_by_token(token))
    data1 = {"discountIds ": dict_res.get('discounts'), "groupActivityId ": 0, "groupPurchaseId ": 0, "trial ": 0,
             "status": 0}
    # 获取最终提交价格
    totalFee_1 = get_entity_price_totalFee(bookid, constant.resourceType_book, token)
    print('最终提交价格：', totalFee_1)
    totalFee_account = str(len(items) * int(totalFee_1))
    # 获取采用听读券金额
    pay = get_user_resource_ticket(bookid, '1', totalFee_account, token)
    parameters_order = {'attach': str(data1),
                        'id': str(bookid),
                        'num': '0',
                        'opType': opType,
                        'outOrderNo': outOrderNo,
                        'totalFee': totalFee_account,
                        'type': ptype
                        }
    if ptype in ['27', '41']:
        parameters_order['items'] = str(items)

    if useTickets == '':
        coin_total_fee = str(pay.get('coin_amount'))
    else:
        coin_total_fee = '0'
    parameters_coinPay = {
        'outOrderNo': outOrderNo,
        'totalFee': coin_total_fee,
        'useTickets': useTickets,
        'useTicketsType': useTicketsType
    }
    order = '/yyting/tradeclient/order.action?' + geturl_haslist(parameters_order)
    coinPay = '/yyting/tradeclient/coinPay.action?' + geturl_haslist(parameters_coinPay)
    endlist = [order, coinPay]
    print('最终入参list', endlist)
    data = {
        'operations': str(endlist).replace(' ', ''),
        'type': 'serial_fail_fast',
        'token': token
    }

    r = httputils.post_app(getApiName('serialOperation'), data)
    print('购买返回数据：', json.loads(r.text))
    res = r.text
    jsonr_dict = json.loads(res)
    result = jsonr_dict['list'][0].get('result')
    dict_result = json.loads(result)
    print('购买最终结果coinPay，：', dict_result.get('data'))
    if str(jsonr_dict.get('status')) == '0':
        return dict_result.get('data').get('orderNo')
    else:
        return dict_result.get('msg')


def buy_albumn_utils(token, bookid: str, items: list, opType: str, ptype: str, useTicketsType: str, useTickets=''):
    """
    购买节目
    :param token:
    :param useTicketsType:用券类型：0-不用券，1-券+余额,2-不用券
    :param bookid:书籍id
    :param items:书籍章节，分章购买章节获取参考get_albumn_chapters方法
    :param opType:Item模式
    :param ptype:购买方式，来自于constant文件
    :return:orderNo，类型为str
    """
    # 登录获取token
    # token = get_app_login_token()
    # 获取资源价格信息
    dict_res = get_entity_price_by_id(bookid, constant.resourceType_albumn)
    # 获取outOrderNo
    outOrderNo = init_uuid()
    # 获取听读券余额
    ticks = get_ticketBalance_by_token(token)
    # 获取账户余额,不够钱自动充值
    headers = getconf.getdict('Headers', 'user-agent')
    if 'Android' in headers.get('user-agent'):
        balance = get_user_account_amount(token, constant.coinType_Andriod)
        print('账户余额', balance)
        if float(balance) + float(ticks) < float(dict_res.get('price')):
            charge_coin_to_user(constant.coinType_Andriod, dict_res.get('price'), get_userid_by_token(token))
    elif 'iOS' in headers.get('user-agent'):
        balance = get_user_account_amount(token, constant.coinType_ios)
        if float(balance) + float(ticks) < float(dict_res.get('price')):
            charge_coin_to_user(constant.coinType_ios, dict_res.get('price'), get_userid_by_token(token))
    data1 = {"discountIds ": dict_res.get('discounts'), "groupActivityId ": 0, "groupPurchaseId ": 0, "trial ": 0,
             "status": 0}
    # 获取最终提交价格
    totalFee_1 = get_entity_price_totalFee(bookid, constant.resourceType_albumn, token)
    totalFee_account = str(len(items) * int(totalFee_1))
    print('总金额：', totalFee_account)
    # 获取采用听读券金额
    pay = get_user_resource_ticket(bookid, '2', totalFee_account, token)
    # totalFee_ticket = '0'
    parameters_order = {'attach': str(data1),
                        'id': str(bookid),
                        'num': '0',
                        'opType': opType,
                        'outOrderNo': outOrderNo,
                        'totalFee': totalFee_account,
                        'type': ptype
                        }
    if ptype in ['27', '41', '25']:
        parameters_order['items'] = str(items)
    if useTickets == '':
        coin_total_fee = str(pay.get('coin_amount'))
    else:
        coin_total_fee = '0'
    parameters_coinPay = {
        'outOrderNo': outOrderNo,
        'totalFee': coin_total_fee,
        'useTickets': useTickets,
        'useTicketsType': useTicketsType
    }
    order = '/yyting/tradeclient/order.action?' + geturl_haslist(parameters_order)
    coinPay = '/yyting/tradeclient/coinPay.action?' + geturl_haslist(parameters_coinPay)
    endlist = [order, coinPay]
    print('最终入参list', endlist)
    data = {
        'operations': str(endlist).replace(' ', ''),
        'type': 'serial_fail_fast',
        'token': token
    }

    r = httputils.post_app(getApiName('serialOperation'), data)
    print('购买返回数据：', r.text)
    res = r.text
    jsonr_dict = json.loads(res)
    result = jsonr_dict['list'][0].get('result')
    dict_result = json.loads(result)
    print(dict_result.get('data'))
    if str(jsonr_dict.get('status')) == '0':
        return dict_result.get('data').get('orderNo')
    else:
        return dict_result.get('msg')


# def purchase_datas_reduction(orderNo, goodid, userid):
#     """
#     购买后数据还原，便于用例重复执行
#     :param orderNo:购买生成的订单号，类型为str
#     :param goodid:购买的商品id，书籍为bookid，节目为albumid
#     :param userid:用户id
#     :return:
#     """
#     dbutil.update('DELETE FROM  t_consume WHERE User_id=%s AND goods_id=%s' % (userid, goodid), 'db_audiobook')
#     order_tb = 'w_order_' + orderNo[-2:]
#     dbutil.update('DELETE FROM %s WHERE id=%s' % (order_tb, orderNo), 'db_audiobook')


def get_user_resource_ticket(entityId, entityType, totalFee, token):
    """
    根据用户账户听读券余额及需支付金额返回
    :param entityId:
    :param entityType:
    :param totalFee:
    :param token:
    :return:
    """
    data = {
        'entityId': entityId,
        'entityType': entityType,
        'pageNum': '1',
        'pageSize': '500',
        'totalFee': totalFee,
        'token': token,
        'mode': '0'
    }
    r = httputils.get_app(getApiName('ResourceTicketList'), data)
    json_dict = json.loads(r.text)
    sum_balance = 0
    for i in json_dict['list']:
        balance = i.get('balance')
        sum_balance = int(balance) + sum_balance
    if sum_balance > int(totalFee):
        return {'coin_amount': '0', 'ticket_amount': totalFee}
    elif sum_balance < int(totalFee):
        coin_amount = int(totalFee) - sum_balance
        return {'coin_amount': coin_amount, 'ticket_amount': sum_balance}
