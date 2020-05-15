from login.templates.users.Get_UserInfo_By_Token import get_userid_by_token
from login.templates.utils import dbutil


# def account_recharge_users(token, coins, cointype):
#     """
#     账户充值
#     :param token:用户token
#     :param coins:充值金额，支持小数点
#     :param cointype:参考constant.py文件
#     :return:
#     """
#     userid = str(get_userid_by_token(token))
#     n = str(userid)[-1]  # 获取UserID的最后一位
#     table = 'w_integral_' + n  # 对应充值表
#     sql_select = 'SELECT %s FROM %s WHERE User_id= %s' % (cointype, table, str(userid))
#     sql = 'INSERT INTO ' + table + ' (user_id,' + cointype + ',last_modify,create_time) VALUES(' + str(
#         userid) + ',' + str(coins) + ',NOW(),NOW())'
#     sql_update = 'UPDATE %s SET %s=%s WHERE User_id=%s' % (table, cointype, str(coins), str(userid))
#     res = dbutil.select(sql_select, 'db_audiobook')
#     if not res:
#         dbutil.update(sql, 'db_audiobook')
#     else:
#         dbutil.update(sql_update, 'db_audiobook')


def get_user_account_amount(token, cointype):
    """
    根据用户ID获取账户余额
    :param cointype,来自于constant文件下的coinType
    :param userid:
    :return:账户余额，类型为float
    """
    userid = str(get_userid_by_token(token))
    n = str(userid)[-1]  # 获取UserID的最后一位
    table = 'w_integral_' + n  # 对应充值表
    if cointype == '0':
        sql_select_coin = 'SELECT coin FROM %s WHERE User_id= %s' % (table, str(userid))
        res = dbutil.select(sql_select_coin, 'db_audiobook')
        if res == ():
            return 0
        else:
            return float(res[0].get('coin'))
    elif cointype == '1':
        sql_select_ios_coin = 'SELECT ios_coin FROM %s WHERE User_id= %s' % (table, str(userid))
        res = dbutil.select(sql_select_ios_coin, 'db_audiobook')
        if res == ():
            return 0
        else:
            return float(res[0].get('ios_coin'))
