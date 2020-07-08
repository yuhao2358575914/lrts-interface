import json
from login.templates.admin.account.adminlogin import login_admin
from login.templates.utils import httputils, confutils
from login.templates.utils.confutils import getAdminName


def add_CopyRight():
    admintoken = login_admin() # 登录admin获取token
    admin_api = getAdminName('partnerEdit') # 获取partnerEdit接口
    print(admin_api)
    data={'id':'',
        'loginName': 'zhoushichuanCp1541',
        'password': 123456,
        'passwordConfirm': 123456,
        'partnerType': 1,
        'cooperatorType': 2,
        'spTypeBook': 0,
        'spTypeReadBook': 1,
        'spTypeAnnoucer': 0,
        'spTypeVIP': 0,
        'spTypeComic': 0,
        'channelEntityId': '',
        'channelEntityName':'',
        'bookEntityId':'',
        'bookEntityName':'',
        'readbookEntityId': 227620,
        'readbookEntityName': '懒人听书029',
        'annoucerEntityId':'',
        'annoucerEntityName':'',
        'comicEntityId':'',
        'comicEntityName':'',
        'partnerStatus': 2,
        'canLogin': 0,
        'identityCode': 99999999444444443333,
        'contactPerson': '版权合作方037',
        'phone': 13800138000,
        'qq':'',
        'email':'',
        'address':'',
        'postcode':'',
        'bankAccountName': '周同学01',
        'bankAccount': 111111111166666666,
        'bankType': 1,
        'bankProvince': 17,
        'bankCity': 285,
        'bankName': '深圳市南山分行',
        'taxType': 0,
        'billType': 1,
        'billCode':'',
        'buttMan': ''
    }
    r = httputils.postadmin(admin_api, data, admintoken, confutils.getcurrentPath('PartnerEdit'))
    print(json.loads(r.text))
if __name__=='__main__':
    add_CopyRight()