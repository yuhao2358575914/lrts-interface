import json

from login.templates.utils import getconf, httputils
from login.templates.utils.confutils import getApiName
from login.templates.utils.utils import get_local_time_str

"""
获取自动注册token-游客模式

"""


def get_auto_register_token_app():
    autoreg = getconf.get_global_conf('apinames', 'autoreg')
    payload = {'regid': 'NDYwMDE2NTc2MjU4MDcx', 'regmei': 'ODY2MjI5MDM1MzY5ODcz'}
    r = httputils.post_app(autoreg, payload)
    if r.status_code == 200:
        return json.loads(r.text)['token']
    else:
        return False

#
# def get_auto_register_token_new():
#     """
#     安卓新版本自动注册获取token
#     :return:
#     """
#     dict_str = {"androidId": "8cec4bacd1a02815", "deviceMd5": "aa48579c6abf700fc22aeffb25674c21",
#                 "imei": "863254010140233", "imsi": "460071402367517", "key": "RVjQF98r", "mac": "02:00:4C:4F:4F:50",
#                 "nowTime": get_local_time_str(), "oaid": "", "oldImei": "ODYzMjU0MDEwMTQwMjMz",
#                 "serialNo": "bacd1a028158cec4", "umengId": "b59fa718cdb5e3b29f4f7a4bfea2f5"}
#     encript_str = rsa_encrypt(str(dict_str))
#     r = httputils.post_reg(getApiName('autoreg'), {'meta': encript_str.decode(encoding="utf-8")})
#     print(r.text)
#     if r.status_code == 200:
#         return json.loads(r.text)['token']
#     else:
#         return False
