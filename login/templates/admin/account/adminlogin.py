"""
admin相关操作

"""

# admin登录
import json
from login.templates.utils import getconf, httputils
from login.templates.utils.confutils import getAdminName, getcurrentPath
from login.templates.utils.encodeutils import encrypt_md5
from login.templates.utils.getconf import get_conf, write_config_ini


def login_admin(username=getconf.get_conf('users', 'adminuser'), pwd=getconf.get_conf('users', 'adminpwd')):
    """
    admin登录
    :return:
    """
    # 前端密碼加密
    encrypt_pwd = encrypt_md5(pwd + '69FzDZZgC%4BWv%AE-l#l~.7')
    admin_token = get_conf('admin', 'admin_token')
    check_code = check_admintoken_by_search(admin_token)
    print('*******CheckCode:重新获取1否则0*******', check_code)
    if check_code == 1 or username != getconf.get_conf('users', 'adminuser'):
        adminDomain = getconf.get_conf('HOST', 'adminDomain')
        r = httputils.postadmin_old(adminDomain, '/platformauth/login',
                                    {'accountName': username, 'password': encrypt_pwd, 'type': '0',
                                     'needReturn': 'true'},
                                    {
                                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
                                        'Content-Type': 'application/x-www-form-urlencoded'})
        token_got = json.loads(r.text)['data']['token']
        print('获取的token', token_got)
        if token_got is not None:
            write_config_ini('admin', "admin_token", token_got)
            return token_got
        else:
            r1 = httputils.postadmin_old(adminDomain, '/platformauth/login',
                                         {'verifyCode': '0000', 'phone': getconf.get_conf('users', 'admin_phone'),
                                          'type': '1', 'needReturn': 'true'},
                                         {
                                             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
                                             'Content-Type': 'application/x-www-form-urlencoded'})
            token_got1 = json.loads(r1.text)['data']['token']
            if token_got1:
                write_config_ini('admin', "admin_token", token_got1)
                return token_got1
    else:
        return admin_token


def check_admintoken_by_search(admin_token):
    """
    检查token是否有效
    :param admin_token:
    :return:
    """
    r = httputils.getadmin(getAdminName('userSearch'),
                           {},
                           admin_token,
                           getcurrentPath('UserManageList'))
    result = json.loads(r.text)
    if result['status'] == 0:
        return 0
    else:
        return 1
