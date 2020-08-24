import pymysql

from login.templates.admin.platform.common.operate_mysql import billing_select, billing_delete
from login.templates.utils import getconf
from login.templates.utils.getconf import get_conf


# def select(sql, dbname):
#     print('****当前SQL****：' + sql)
#     apidomain = getconf.get_conf("HOST", "apidomain")
#     print(apidomain, type(apidomain))
#     if "earth" in apidomain:
#         host = getconf.get_conf("mysql_earth", "host")
#         user = getconf.get_conf("mysql_earth", "username")
#         password = getconf.get_conf("mysql_earth", "password")
#         db=getconf.get_conf("mysql_earth", str(dbname))
#     else:
#         host = getconf.get_conf("mysql_moon", "host")
#         user = getconf.get_conf("mysql_moon", "username")
#         password = getconf.get_conf("mysql_moon", "password")
#         db = getconf.get_conf("mysql_moon", str(dbname))
#     print('host',host)
#     print('user',user)
#     print('password',password)
#     print('db',db)
#
#     try:
#         connection = pymysql.connect(host=host,
#                                      user=user,
#                                      password=password,
#                                      db=db,
#                                      charset='utf8mb4',
#                                      cursorclass=pymysql.cursors.DictCursor)
#         cur = connection.cursor()
#         cur.execute(sql)
#         result = cur.fetchall()
#         print(result)
#         return result
#     except Exception as e:
#         print('查询出错:%s' % e)
#     finally:
#         cur.close()
#         connection.close()

# def select(sql, dbname, host=getconf.get_conf("mysql_moon", "host"), user=getconf.get_conf("mysql_moon", "username"),
#            password=getconf.get_conf("mysql_moon", "password")):
#     print('****当前SQL****：' + sql)
#     try:
#         connection = pymysql.connect(host=host,
#                                      user=user,
#                                      password=password,
#                                      db=getconf.get_conf("mysql_moon", dbname),
#                                      charset='utf8mb4',
#                                      cursorclass=pymysql.cursors.DictCursor)
#         cursor = connection.cursor()
#         cursor.execute(sql)
#         result = cursor.fetchall()
#         print(result)
#         return result
#     except Exception as e:
#         print('查询出错:%s' % e)
#     finally:
#         cursor.close()
#         connection.close()

# def billing_select(sql, db):
#     '''billing,readbook,platform库查询
#     :param sql 数据库语句
#     :param db 数据库名称
#     :return list
#     '''
#     apidomain = getconf.get_conf("HOST", "apidomain")
#     print(apidomain, type(apidomain))
#     if "earth" in apidomain:
#         host = getconf.get_conf("mysql_earth", "host")
#         user = getconf.get_conf("mysql_earth", "username"),
#         password = getconf.get_conf("mysql_earth", "password")
#         db = getconf.get_conf("mysql_earth", str(db))
#     else:
#         host = getconf.get_conf("mysql_moon", "host")
#         user = getconf.get_conf("mysql_moon", "username"),
#         password = getconf.get_conf("mysql_moon", "password")
#         db = getconf.get_conf("mysql_moon", str(db))
#     conn = pymysql.connect(host=host, user=user,
#                            password=password, database=db, charset='utf8mb4')
#     cur = conn.cursor(cursorclass=pymysql.cursors.DictCursor)
#     cur.execute(sql)
#     res = cur.fetchall()
#     cur.close()
#     conn.close()
#     print(type(res))
#     print(res)
#     return res
import json
import unittest
import random

from login.templates.admin.account.adminlogin import login_admin
from login.templates.admin.platform.common.Add_Announcer import add_Announcer
from login.templates.admin.platform.common.Create_Number import create_IDNumber, create_PhoneNum, \
    create_CreditCardNumbers
from login.templates.admin.platform.common.Create_PartnerName import partnerName
from login.templates.admin.platform.common.operate_mysql import billing_select
from login.templates.utils import httputils, confutils
from login.templates.utils.confutils import getAdminName
# 生成随机字符串
def random_chinese(num):
    str_chinesse=[]
    for i in range(num):
        head = random.randint(0xb0, 0xf7)
        body = random.randint(0xa1, 0xfe)
        val = f'{head:x} {body:x}'
        str = bytes.fromhex(val).decode('gb2312')
        str_chinesse.append(str)
    str_final="".join(str_chinesse)
    print(str_final)
    return str_final


if __name__ == '__main__':
    random_chinese(4)





