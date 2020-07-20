import json
import unittest

from login.templates.admin.book.Book_Operation import edit_book_info_by_dict, operation_book_get_freecharpters
from login.templates.app.account.Get_Logon_Token import get_app_login_token
from login.templates.app.common.Get_Book_By_User import user_get_book_purchased
from login.templates.utils import httputils
from login.templates.utils.confutils import getApiName

"""

有声书籍A勾选【下架后已购用户免费章节不可见】，书籍A下线后，已购用户不可见免费章节

"""


class case_Book_Free_Chapters_For_Purchased_Users_Not(unittest.TestCase):
    def test_Book_Free_Chapters_For_Purchased_Users_Not(self):
        '''有声书籍A勾选【下架后已购用户免费章节不可见】，书籍A下线后，已购用户不可见免费章节'''
        # 登录并获取token
        token = get_app_login_token()
        # 获取一本用户已购书籍
        bookid = user_get_book_purchased(token)
        if bookid != 0:
            # 数据处理(1、书籍下线2、设置【下架后已购用户免费章节不可见】3、调整书籍为正序)
            msg = edit_book_info_by_dict(str(bookid), {'bState': '1', 'canNotFreeSection': 'true', 'sort': '0'})
            # 获取书籍免费章节
            freecharps = operation_book_get_freecharpters(bookid)
            print('起始免费章节', freecharps)
            # 拼接入参data
            data = {'sortType': '0',
                    'bookId': '37717', 'isUp': '0', 'pageNum': '1', 'pageSize': '50', 'token': token}
            r = httputils.get_app(getApiName('ClientGetBookResource'), data)
            print(r.json())
            self.assertEqual(json.loads(r.text)['status'], 0, '请求失败')
            self.assertEqual(json.loads(r.text)['list'][0]['state'], -2, '免费章节未过滤')
        else:
            print('当前用户未购任何书籍！')
            self.assertFalse()


if __name__ == '__main__':
    unittest.main()
