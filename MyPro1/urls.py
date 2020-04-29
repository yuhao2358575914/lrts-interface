"""MyPro1 URL Configuration

The `urlpatterns` list routes URLs to viewas. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function viewas
    1. Add an import:  from my_app import viewas
    2. Add a URL to urlpatterns:  path('', viewas.home, name='home')
Class-based viewas
    1. Add an import:  from other_app.viewas import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from login import views
from login.viewas.lazy_view import activitys_view
from login.viewas.lazy_view import user_view
from login.viewas.test_view import autotest_view
from login.viewas.test_view import cases_views

from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('pages/', views.pages),
    path('pages/', views.error),
    path('login/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
    path('add_cases/', cases_views.add_cases),
    path('cases_detail/', cases_views.cases_detail),
    path('search_case/', cases_views.search_case),
    path('delete_case/', cases_views.delete_case),
    path('case_edit/', cases_views.case_edit),
    path('api_test/', autotest_view.api_test),
    path('run_test/', autotest_view.run_test),
    path('test_report/', autotest_view.test_report),
    path('test_report_single/', autotest_view.test_report_single),
    path('send_email/', autotest_view.send_email),
    path('run_case/', autotest_view.run_case),
    path('send_vip/', user_view.send_vip),
    path('vip_expire/', user_view.vip_expire),
    path('send_code/', user_view.send_code),
    path('charge_account/', user_view.charge_account),
    path('add_buy_share/', activitys_view.add_buy_share),
    path('add_ShareListen_free/', activitys_view.add_ShareListen_free),
    path('add_Subtracts_activity/', activitys_view.add_Subtracts_activity),
    path('activity_list/', activitys_view.activity_list),
    path('lazy_reg/', views.lazy_reg),
    path('get_config/', views.get_config),
    # path('crypt_utils/',viewas.crypt_utils),
    path('error/', views.error),
    path('get_ips/', views.get_ips),
    path('captcha/', include('captcha.urls'))
]
