import random

from login.templates.users.Get_UserInfo_By_Token import get_userid_by_token
from login.templates.utils import dbutil

"""
获取用户已购书籍
"""
def user_get_book_purchased(token):
    result = dbutil.select('SELECT goods_id FROM t_consume WHERE TYPE=2 AND user_id ='+str(get_userid_by_token(token)),'db_audiobook')
    print('已购书籍列表为：',result)
    if result:
        return str(result[random.randint(0,len(result)-1)].get('goods_id'))
    else:
        return 0
