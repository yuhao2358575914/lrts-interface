import unittest

from login.templates.app.account.Get_Logon_Token import get_app_login_token


class Case_Necessary_Account_Password_Login(unittest.TestCase):
    def test_Necessary_Account_Password_Login(self):
        '''手机号登录-必测用例'''
        # 手机号注册
        token = get_app_login_token()
        self.assertIsNotNone(token)


if __name__ == '__main__':
    unittest.main()
