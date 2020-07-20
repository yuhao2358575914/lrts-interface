import pymysql
from login.templates.utils.getconf import get_conf


def select(sql, db):
    '''audiobook、yyting_partdb库查询
    :param sql 数据库语句
    :param db 数据库名称
    '''
    conn = pymysql.connect(host=get_conf('mysql', 'host'), user=get_conf('mysql', 'username'),
                           password=get_conf('mysql', 'password'), database=db, charset='utf8mb4')
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cur.execute(sql)
    res = cur.fetchall()
    cur.close()
    conn.close()
    print(type(res))
    print(res)
    return res


def billing_select(sql, db):
    '''billing,readbook,platform库查询
    :param sql 数据库语句
    :param db 数据库名称
    '''
    conn = pymysql.connect(host=get_conf('moon_billing', 'host'), user=get_conf('moon_billing', 'username'),
                           password=get_conf('moon_billing', 'password'), database=db, charset='utf8mb4')
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cur.execute(sql)
    res = cur.fetchall()
    cur.close()
    conn.close()
    print(type(res))
    print(res)
    return res
