# 自建的路由文件
# 导入path来匹配url
from django.urls import path
# 导入当前目录下的views

# 确定命名空间
from .viewas.platform_views import copyright_views, channel_views, anchor_views, date_views, randomNum_views, \
    settlement_views, settlement_vip_views

app_name = 'login'
# 子路由表
urlpatterns = [
    # path()负责绑定业务功能
    # 第一个参数是url,url里的参数用'< >'包裹
    # 第二个参数是绑定的业务功能，xxx.as_view()把xxx类作为业务功能
    # 第三个参数代表该条url的名字
    path('add_copyright_partner', copyright_views.add_copyright_partner),
    path('add_channel_partner', channel_views.add_channel_partner),
    path('add_anchor_partner', anchor_views.add_anchor_partner),
    path('add_develop_channel', channel_views.add_develop_channel),
    path('month_day', date_views.month_day),
    path('randomNum', randomNum_views.create_random_num),
    path('settlement_not_vip', settlement_views.settlement_not_vip),
    path('settlement_not_vip_result', settlement_views.settlement_not_vip_result),
    path('settlement_vip', settlement_vip_views.settlement_vip),
    path('settlement_vip_result', settlement_vip_views.settlement_vip_result),
    # path('settlement_vip_result', settlement_vip_views.settlement_vip_result),
]