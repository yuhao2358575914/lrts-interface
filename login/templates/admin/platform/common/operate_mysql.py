import pymysql
from login.templates.utils.getconf import get_conf


def select(sql, db):
    '''audiobook、yyting_partdb库查询
    :param sql 数据库语句
    :param db 数据库名称
    :return list
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
    :return list
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
def billing_delete(sql, db):
    '''billing,readbook,platform库删除操作
    :param sql 数据库语句
    :param db 数据库名称
    :return list
    '''
    conn = pymysql.connect(host=get_conf('moon_billing', 'host'), user=get_conf('moon_billing', 'username'),
                           password=get_conf('moon_billing', 'password'), database=db, charset='utf8mb4')
    #使用cursor()方法获取操作游标
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        #执行sql语句
        cur.execute(sql)
        #提交修改
        conn.commit()
    except:
        # 发生错误时回滚
        cur.rollback()
    # 关闭连接
    conn.close()
    cur.close()
