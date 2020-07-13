import pymysql
from login.templates.utils.getconf import get_conf


def select(sql,db):
    '''audiobook、yyting_partdb库查询
    :param sql 数据库语句
    :param db 数据库名称
    '''
    conn = pymysql.connect(host=get_conf('moon','host'), user=get_conf('moon','username'), password=get_conf('moon','password'), database=db,charset='utf8mb4')
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cur.execute(sql)
    res = cur.fetchall()
    cur.close()
    conn.close()
    print(type(res))
    print(res)
    return  res
def billing_select(sql,db):
    '''billing,readbook,platform库查询
    :param sql 数据库语句
    :param db 数据库名称
    '''
    conn = pymysql.connect(host=get_conf('moon_billing','host'), user=get_conf('moon_billing','username'), password=get_conf('moon_billing','password'), database=db,charset='utf8mb4')
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cur.execute(sql)
    res = cur.fetchall()
    cur.close()
    conn.close()
    print(type(res))
    print(res)
    return  res

# def billing_select(sql):
#     '''billing库查询'''
#     conn = pymysql.connect(host=get_conf('moon_billing','host'), user=get_conf('moon_billing','username'), password=get_conf('moon_billing','password'), database="billing",charset='utf8mb4')
#     cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
#     cur.execute(sql)
#     res = cur.fetchall()
#     cur.close()
#     conn.close()
#     print(type(res))
#     return  res
# def readbook_select(sql):
#     '''readbook库（电子阅读版权）查询'''
#     conn = pymysql.connect(host=get_conf('readbook','host'), user=get_conf('readbook','username_readbook'), password=get_conf('readbook','password_readbook'), database="readbook",charset='utf8mb4')
#     cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
#     cur.execute(sql)
#     res = cur.fetchall()
#     cur.close()
#     conn.close()
#     print(type(res))
#     return  res
# def platform_select(sql):
#     '''platform库播音查询'''
#     conn = pymysql.connect(host=get_conf('moon_billing', 'host'), user=get_conf('moon_billing', 'username'),password=get_conf('moon_billing', 'password'), database="platform", charset='utf8mb4')
#     cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
#     cur.execute(sql)
#     res = cur.fetchall()
#     cur.close()
#     conn.close()
#     print(type(res))
#     return res

if __name__=='__main__':
    billing_select("SELECT * from p_partner ORDER BY id desc LIMIT 1;",'billing')