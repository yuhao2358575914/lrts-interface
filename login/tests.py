import requests
from django.test import TestCase

# Create your tests here.
from login.templates.admin.activities.activityBuyShare import add_BuyShare_activity
from login.templates.admin.book.Book_Operation import get_book_by_pay_type
#
# a=add_BuyShare_activity(get_book_by_pay_type(1,3),get_book_by_pay_type(2,3))
# print(a)