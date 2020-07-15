import unittest

from login.templates.users.User import init_register_user_by_phone


class Case_Necessary_Phone_Number_Register(unittest.TestCase):
    def test_Necessary_Phone_Number_Register(self):
        '''手机号注册-必测用例'''
        # 手机号注册
        userid = init_register_user_by_phone()
        self.assertIsNotNone(userid)


if __name__ == '__main__':
    unittest.main()
