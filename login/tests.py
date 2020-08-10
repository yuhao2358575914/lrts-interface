import datetime
import os
import re

import requests
from django.test import TestCase

# Create your tests here.
from login.run.run_test import run_test_bf
from login.templates.admin.account.adminlogin import login_admin
from login.templates.admin.account.user_account import charge_coin_to_user
from login.templates.admin.activities.activityBuyShare import add_BuyShare_activity
from login.templates.admin.activities.send_code import add_vip_exchange_code, send_vip_by_exchangeCode, \
    approve_listen_tickets
from login.templates.admin.book.Book_Operation import get_book_by_pay_type, operation_book_get_unbuyedcharpters_all, \
    operation_book_get_buyedcharpters_all, operation_book_get_freecharpters

#
# a=add_BuyShare_activity(get_book_by_pay_type(1,3),get_book_by_pay_type(2,3))
# print(a)
# params = '/yyting/page/recommendPage.action?pageVersion=v3&recommendedSwitch=0&type=2&token=JTa_wEdSIhzP1SZKF6GjFg**_gtSvJSSO3svh93sMwoQnezwJTTOmUT-m&imei=ODYzMjU0MDEwMTQwMjMz&nwt=1&q=474&mode=0&sc=67f156dc6a39b5884ab7f0c5a0c39695'
# s1 = params.split('?')[1].split('&')
# param_dict = {}
# for i in s1:
#     s2 = i.split('=')
#     if s2[0] != 'sc':
#         param_dict[s2[0]] = s2[1]
# class_name = os.path.basename(__file__)
# print(class_name)
# aa=run_test_bf('case_Search_Normal_Word.py')
# print(aa)
# print(type(aa))
# charpters = operation_book_get_unbuyedcharpters_all('92365489', 'MFyzOz-LtD7P1SZKF6GjFg**_qKkiCdyyMrjjDGxUh_yuZP2hbkAc4-6o')
# print(charpters)
# from login.templates.app.order.Entity_Price import get_entity_price_by_id
# from login.templates.users.Get_UserInfo_By_Token import get_userid_by_token
# token = 'M_2_2bkYZr7P1SZKF6GjFg**_gtSvJSSO3suJw7sB7aTQBX0Vfy9LgB7Z'
# charpters = operation_book_get_unbuyedcharpters_all('92365489', token)
# buy=operation_book_get_buyedcharpters_all('92365489', token)
# free=operation_book_get_freecharpters('92365489')
# print(charpters)
# print(buy)
# print(free)
from login.templates.utils import getconf
# 买vip
# r = requests.get(
#     'http://192.168.3.158:8084/yytingopenapi/order/createOrder?totalFee=1500&goodsId=1&phoneNum=15959082192&partnerId=200429001579&goodsNum=1&shareFee=233&outOrderNum=VJ511r6s122H411&goodsType=3&token=82c8fdd4d2f747a90934a22a87b8403b',
#     headers=getconf.getdict('Headers', 'user-agent'))
# print(r.text)
# print(r.status_code)

# 买书
# r = requests.get(
#     'http://192.168.3.158:8084/yytingopenapi/order/createOrder?totalFee=1500&goodsId=32201&phoneNum=15959082192&partnerId=200429001579&goodsNum=48&shareFee=233&outOrderNum=VJ66r21122H311&goodsType=4&token=82c8fdd4d2f747a90934a22a87b8403b',
#     headers=getconf.getdict('Headers', 'user-agent'))
# print(r.text)
# print(r.status_code)

# 买vip
# r = requests.get(
#     'http://moon-openapi.lrts.me/order/createOrder?totalFee=4200&goodsId=3&phoneNum=15959082191&partnerId=200429001579&goodsNum=1&shareFee=233&outOrderNum=VJ52GGWb11H221&goodsType=3&token=82c8fdd4d2f747a90934a22a87b8403b',
#     headers=getconf.getdict('Headers', 'user-agent'))
# print(r.text)
# print(r.status_code)


# 充值
# r = requests.get(
#     'http://192.168.3.158:8084/yytingopenapi/order/createOrder?totalFee=1000&goodsId=1&phoneNum=15959082194&partnerId=200429001579&goodsNum=100&shareFee=233&outOrderNum=VT67r1k1edge2&goodsType=2&token=82c8fdd4d2f747a90934a22a87b8403b',
#     headers=getconf.getdict('Headers', 'user-agent'))
# print(r.text)
# print(r.status_code)


# r = requests.get(
#     'http://moon-openapi.lrts.me/open/oauth2/accessToken?appId=200429001579&secret=U?YXFAcwmzrtUe%CbxcdRFGF&code=epMSMr3QADeBL5txsLlv78WY8GOogNUuTbeD32lqnj1xsQGVvaWXE+69vBGLdJNjQ/fKa124oZM4Tc14ZvCAfDCFBhKbs/WI7GTz9VYUsiP1H0zKYMtxLQ==',
#     headers=getconf.getdict('Headers', 'user-agent'))
# print(r.text)
# print(r.status_code)


#############天猫精灵app下单##############
#买书-分章节
# r = requests.get(
#         'http://moon-openapi.lrts.me/open/oauth2/tmall/createOrder?openId=aUKe%2bHKJ7CtPvR%2b8X8DDvpY8%2bbEUJ9fXILo40f8sX8ta2InOddIWzO5XRjGkHbKQ&accessToken=3WRChlp9FQLM9%2fWhnsSzvzfvtIAsEIg%2fszTtRtGOjFyvUDTQTvljGD2hBCXujtPrDaJN4dyKLsfudyNPJ60evw4vgWGexBNwewnlcAteLHHhbhf5VbOVfy3hkHOWgwi%2bz8i%2f2n%2bezR9Q0ZippFY6V8%2b8Tg88asv1SZRm1BcOT0S8QDZZEbPUkg%3d%3d&totalFee=2&goodsId=10003308600055&payTime=1594436206000&appId=200429001579&shareFee=1&outOrderNum=asd71311221452&goodsType=1&token=82c8fdd4d2f747a90934a22a87b8403b',
#     headers=getconf.getdict('Headers', 'user-agent'))
# print(r.text)
# print(r.status_code)


#买书-整本
# r = requests.get(
#         'http://moon-openapi.lrts.me/open/oauth2/tmall/createOrder?openId=aUKe%2bHKJ7CtPvR%2b8X8DDvpY8%2bbEUJ9fXILo40f8sX8ta2InOddIWzO5XRjGkHbKQ&accessToken=3WRChlp9FQLM9%2fWhnsSzvzfvtIAsEIg%2fszTtRtGOjFyvUDTQTvljGD2hBCXujtPrDaJN4dyKLsfudyNPJ60evw4vgWGexBNwewnlcAteLHHhbhf5VbOVfy3hkHOWgwi%2bz8i%2f2n%2bezR9Q0ZippFY6V8%2b8Tg88asv1SZRm1BcOT0S8QDZZEbPUkg%3d%3d&totalFee=2&goodsId=54343796&payTime=1594436206000&appId=200429001579&shareFee=1&outOrderNum=asd713338114100&goodsType=2&token=82c8fdd4d2f747a90934a22a87b8403b',
#     headers=getconf.getdict('Headers', 'user-agent'))
# print(r.text)
# print(r.status_code)

#买vip
# r = requests.get(
#         'http://moon-openapi.lrts.me/open/oauth2/tmall/createOrder?openId=aUKe%2bHKJ7CtPvR%2b8X8DDvpY8%2bbEUJ9fXILo40f8sX8ta2InOddIWzO5XRjGkHbKQ&accessToken=3WRChlp9FQLM9%2fWhnsSzvzfvtIAsEIg%2fszTtRtGOjFyvUDTQTvljGD2hBCXujtPrDaJN4dyKLsfudyNPJ60evw4vgWGexBNwewnlcAteLHHhbhf5VbOVfy3hkHOWgwi%2bz8i%2f2n%2bezR9Q0ZippFY6V8%2b8Tg88asv1SZRm1BcOT0S8QDZZEbPUkg%3d%3d&totalFee=3&goodsId=vip_30&payTime=1594436206000&appId=200429001579&shareFee=2&outOrderNum=asd713sds8114519&goodsType=3&token=82c8fdd4d2f747a90934a22a87b8403b&os=1',
#     headers=getconf.getdict('Headers', 'user-agent'))
# print(r.text)
# print(r.status_code)

