import json
import unittest
import random
from login.templates.admin.account.adminlogin import login_admin
from login.templates.admin.platform.add_Partner.Add_CopyrightPartner import add_CopyrightPartner
from login.templates.admin.platform.common.Add_CopyRight import add_AudioBookCopyright, add_ReadBookCopyright, \
    add_ComicCopyright
from login.templates.admin.platform.common.Create_Number import create_IDNumber, create_PhoneNum, \
    create_CreditCardNumbers
from login.templates.admin.platform.common.Create_PartnerName import partnerName
from login.templates.admin.platform.common.operate_mysql import billing_select, billing_delete
from login.templates.utils import httputils, confutils
from login.templates.utils.confutils import getAdminName
import ddt

from login.templates.utils.httputils import getadmin


@ddt.ddt  #装饰测试类
class Add_CopyrightParter(unittest.TestCase):

    # @ddt.ddt({'business':1,'partnerType':2},{'business':3,'partnerType':2})
    def setUp(self):
        pass
    def tearDown(self):
        '''数据还原'''
        billing_delete("DELETE from p_partner where login_name='zhoushichuanCpTest';", 'billing')  # 删除p_partner表数据
        billing_delete("DELETE from p_partner_service where entity_id='6105';",'billing')  # 删除p_partner_service表数据

    @ddt.data((1, 2), (3,2)) #装饰测试方法
    @ddt.unpack

    def test_add_CopyrightPartner(self,business, partnerType):
        '''添加版权合作方
    :param business 0表示勾选全部业务 1表示付费收听 2 表示电子阅读 3表示VIP会员 4 表示漫画
    :param partnerType 1表示个人账户 2表示公司账户
    '''
        admintoken = login_admin()  # 登录admin获取token
        admin_api = getAdminName('partnerEdit')  # 获取partnerEdit接口
        print(admin_api)
        # 数据准备
        data = {}
        PartnerName_Record = partnerName(2)  # 生成版权合作方
        PartnerName = PartnerName_Record[0]  # 生成一个新的版权合作方名称
        PartnerName_Number = PartnerName_Record[1]  # 获取新的版权合作方名称后面的数字
        # 判断是个人账户还是公司账户
        if partnerType == 1:
            data['contactPerson'] = PartnerName + '(个人账户)'
        elif partnerType == 2:
            data['fullName'] = PartnerName + '(公司账户)'
            data['shortName'] = PartnerName + '(公司账户)'
            data['contactPerson'] = PartnerName + '(公司账户)'
            data['deductTaxRate'] = random.randint(2, 20)
        else:
            print('账户类型输入有误！！！')
        if business == 0:
            book_cp = add_AudioBookCopyright()  # 获取书籍版权信息
            book_cp_id = book_cp[0]  # 获取书籍版权id
            book_cp_name = book_cp[1]  # 获取书籍版权name
            readbook_cp = add_ReadBookCopyright()  # 获取电子阅读版权信息
            readbook_cp_id = str(readbook_cp[0])  # 获取电子阅读版权id
            readbook_cp_name = readbook_cp[1]  # 获取电子阅读版权name
            comic_cp = add_ComicCopyright()  # 获取漫画版权信息
            comic_cp_id = str(comic_cp[0])  # 获取漫画版权id
            comic_cp_name = comic_cp[1]  # 获取漫画版权name
            data['spTypeBook'] = 1
            data['spTypeReadBook'] = 1
            data['spTypeVIP'] = 1
            data['spTypeComic'] = 1
            data['readbookEntityId'] = readbook_cp_id
            data['readbookEntityName'] = readbook_cp_name
            data['comicEntityId'] = comic_cp_id
            data['comicEntityName'] = comic_cp_name
            data['bookEntityId'] = book_cp_id
            data['bookEntityName'] = book_cp_name
        elif business == 1:
            # book_cp = add_AudioBookCopyright()  # 获取版权信息
            book_cp_id = 6105  # 获取版权id
            book_cp_name = '有声书籍版权6105'  # 获取版权name
            data['spTypeBook'] = 1
            data['spTypeReadBook'] = 0
            data['spTypeVIP'] = 0
            data['spTypeComic'] = 0
            data['readbookEntityId'] = ''
            data['readbookEntityName'] = ''
            data['comicEntityId'] = ''
            data['comicEntityName'] = ''
            data['bookEntityId'] = book_cp_id
            data['bookEntityName'] = book_cp_name
        elif business == 2:
            readbook_cp = add_ReadBookCopyright()  # 获取版权信息
            readbook_cp_id = str(readbook_cp[0])  # 获取版权id
            readbook_cp_name = readbook_cp[1]  # 获取版权name
            data['spTypeBook'] = 0
            data['spTypeReadBook'] = 1
            data['spTypeVIP'] = 0
            data['spTypeComic'] = 0
            data['bookEntityId'] = ''
            data['bookEntityName'] = ''
            data['comicEntityId'] = ''
            data['comicEntityName'] = ''
            data['readbookEntityId'] = readbook_cp_id
            data['readbookEntityName'] = readbook_cp_name
        elif business == 3:
            # book_cp = add_AudioBookCopyright()  # 获取版权信息
            book_cp_id = 6105  # 获取版权id
            book_cp_name = '有声书籍版权6105'  # 获取版权name
            data['spTypeBook'] = 0
            data['spTypeReadBook'] = 0
            data['spTypeVIP'] = 1
            data['spTypeComic'] = 0
            data['readbookEntityId'] = ''
            data['readbookEntityName'] = ''
            data['comicEntityId'] = ''
            data['comicEntityName'] = ''
            data['bookEntityId'] = book_cp_id
            data['bookEntityName'] = book_cp_name
        elif business == 4:
            comic_cp = add_ComicCopyright()  # 获取版权信息
            comic_cp_id = str(comic_cp[0])  # 获取版权id
            comic_cp_name = comic_cp[1]  # 获取版权name
            data['spTypeBook'] = 0
            data['spTypeReadBook'] = 0
            data['spTypeVIP'] = 0
            data['spTypeComic'] = 1
            data['readbookEntityId'] = ''
            data['readbookEntityName'] = ''
            data['bookEntityId'] = ''
            data['bookEntityName'] = ''
            data['comicEntityId'] = comic_cp_id
            data['comicEntityName'] = comic_cp_name
        else:
            print('传参错误，请重新输入！！！')
        # 接口入参
        data['id'] = ''
        data['channelEntityId'] = ''
        data['channelEntityName'] = ''
        data['annoucerEntityId'] = ''
        data['annoucerEntityName'] = ''
        data['partnerStatus'] = 2
        data['canLogin'] = 0
        data['identityCode'] = create_IDNumber()
        data['phone'] = create_PhoneNum()
        data['qq'] = ''
        data['email'] = ''
        data['address'] = '深圳市南山区粤海街道'
        data['postcode'] = ''
        data['bankAccount'] = create_CreditCardNumbers()
        data['bankType'] = 1  # 1表示中国银行
        data['bankProvince'] = 7
        data['bankCity'] = 152
        data['bankName'] = '深圳市中国银行南山分行'
        data['taxType'] = 0
        data['billType'] = 1
        data['billCode'] = ''
        data['buttMan'] = ''
        data['loginName'] = 'zhoushichuanCpTest'
        data['password'] = 123456
        data['passwordConfirm'] = 123456
        data['partnerType'] = partnerType  # 1表示个人账户 2表示公司账户
        data['cooperatorType'] = 2  # 1渠道 2版权 3主播
        data['spTypeAnnoucer'] = 0
        data['bankAccountName'] = '周同学01'
        # 发送post请求
        r = httputils.postadmin(admin_api, data, admintoken, confutils.getcurrentPath('PartnerEdit'))
        res = json.loads(r.text)
        print(res)
        self.assertTrue(res['status'] == 0 and res['error'] == False, '测试失败!!!')
        print('----------------版权合作方添加成功！！！------------------')


if __name__=='__main__':
    unittest.main()
