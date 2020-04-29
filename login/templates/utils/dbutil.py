# coding=utf-8
import pymysql.cursors
from login.templates.utils import getconf


# 查
def select(sql, dbname, host=getconf.get_conf("mysql", "host"), user=getconf.get_conf("mysql", "username"),
           password=getconf.get_conf("mysql", "password")):
    print('****当前SQL****：' + sql)
    connection = pymysql.connect(host=host,
                                 user=user,
                                 password=password,
                                 db=getconf.get_conf("mysql", dbname),
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    connection.close()
    return result


# 改
def update(sql, dbname, host=getconf.get_conf("mysql", "host"), user=getconf.get_conf("mysql", "username"),
           password=getconf.get_conf("mysql", "password")):
    print('****当前SQL****：' + sql)
    connection = pymysql.connect(host=host,
                                 user=user,
                                 password=password,
                                 db=getconf.get_conf("mysql", dbname),
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    connection.close()
