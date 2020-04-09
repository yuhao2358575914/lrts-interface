"""MyPro1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from login import views
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('pages/', views.pages),
    path('pages/', views.error),
    path('login/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
    path('api_test/', views.api_test),
    path('send_code/', views.send_code),
    path('lazy_reg/', views.lazy_reg),
    path('get_config/', views.get_config),
    # path('crypt_utils/',views.crypt_utils),
    path('error/', views.error),
    path('test_report/', views.test_report),
    path('run_test/', views.run_test),
    path('get_ips/', views.get_ips),
    path('send_email/', views.send_email),
    path('add_cases/', views.add_cases),
    path('cases_detail/', views.cases_detail),
    path('delete_case/', views.delete_case),
    path('run_case/', views.run_case),
    path('case_edit/', views.case_edit),
    path('send_vip/', views.send_vip),
    path('vip_expire/', views.vip_expire),
    path('add_buy_share/', views.add_buy_share),
    path('add_ShareListen_free/', views.add_ShareListen_free),
    path('add_Subtracts_activity/', views.add_Subtracts_activity),
    path('activity_list/', views.activity_list),
    path('captcha/', include('captcha.urls'))
]
