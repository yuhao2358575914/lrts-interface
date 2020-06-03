import re

from django.db import connection
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
import hashlib
from login import models, forms
from login.models import IpUtils, EventInfo, Report_Results

from login.templates.users.User import init_register_user_by_phone
from login.templates.utils import utils
from login.templates.utils.getconf import write_config_ini, get_config_info
from login.templates.utils.utils import get_local_time_second


def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def index(request):
    now_time = utils.get_local_time_second()
    return render(request, 'login/index.html', locals())


def pages(request):
    pass
    return render(request, 'login/forms.html')


def error(request):
    return render(request, 'login/error.html')


def login(request):
    if not request.session.is_empty():
        return redirect('/index/')
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
        try:
            user = models.User.objects.get(name=username)
        except:
            message = '用户不存在！'
            return render(request, 'login/login.html', locals())
        if user.password == hash_code(password):
            request.session['is_login'] = True
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            request.session['role'] = user.role
            return redirect('/index/')
        else:
            message = '密码不正确！'
            return render(request, 'login/login.html', locals())
    login_form = forms.UserForm
    return render(request, 'login/login.html', locals())


def register(request):
    # if request.session.is_empty():
    #     return redirect('/login/')
    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            role = register_form.cleaned_data.get('role')
            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'login/register.html', locals())
            # elif len(password1) < 8:
            #     message = '密码长度小于8位'
            #     return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'login/register.html', locals())
                check = re.compile(r'^[a-z0-9A-Z]+[-|a-z0-9A-Z._]+@lazyaudio.com$')
                if not check.search(email):
                    message = '请使用懒人邮箱！'
                    return render(request, 'login/register.html', locals())
                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.role = role
                new_user.save()
                return redirect('/login')
        else:
            return render(request, 'login/register.html', locals())
    register_form = forms.RegisterForm
    return render(request, 'login/register.html', locals())


def lazy_reg(request):
    """
    手机号注册懒人账号
    :param request:
    :return:
    """
    if request.session.is_empty():
        return redirect('/login/')
    reg_msg = init_register_user_by_phone()
    return render(request, 'login/lazy_reg.html', reg_msg)


def get_config(request):
    """
    获取配置信息
    :param request:
    :return:
    """
    if request.session.is_empty():
        return redirect('/login/')
    res_msg = get_config_info()
    return render(request, 'login/config.html', {'res_msg': res_msg})


# def crypt_utils(request):
#     # if not request.session['is_login']:
#     #     return redirect('/index/')
#     if request.method == 'POST':
#         crypt_form = forms.CryptUtils(request.POST)
#         if crypt_form.is_valid():
#             crypt_msg = crypt_form.cleaned_data.get('crypt_msg')
#             if not crypt_msg:
#                 message = '加解密信息必填！'
#             crypt_type = crypt_form.cleaned_data.get('crypt_type')
#             if crypt_type == '加密':
#                 result = rsa_encrypt(crypt_msg)
#             elif crypt_type == '解密':
#                 result = rsa_decrypt(crypt_msg)
#             print(result)
#             return render(request, 'login/cript_detail.html', locals())
#         return render(request, 'login/cript_utils.html', locals())
#     return render(request, 'login/cript_utils.html', locals())


def logout(request):
    # if not request.session['is_login']:
    #     return redirect('/login/')
    request.session.flush()
    return redirect("/login/")


def get_ips(request):
    """
    获取用户ip
    :param request:
    :return:
    """
    # if request.session.is_empty():
    #     return redirect('/login/')
    # if request.session.get('role') != '2':
    #     message = '没有权限！'
    #     return render(request, 'login/ip_info.html', locals())
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip_name = request.META.get("HTTP_X_FORWARDED_FOR")
    else:
        ip_name = request.META.get("REMOTE_ADDR")
    search = IpUtils.objects.filter(ip=ip_name)
    if not search:
        local_time = get_local_time_second()
        ips = models.IpUtils()
        ips.ip = ip_name
        ips.login_time = local_time
        ips.save()
    return render(request, 'login/ip_info.html', locals())


def init_env(host_name):
    """
    配置修改
    :param host_name:
    :return:
    """
    write_config_ini('HOST', 'apidomain', host_name.split(',')[0])
    write_config_ini('HOST', 'admindomain', host_name.split(',')[1])


def echarts_data(request):
    """
    自动化测试结果图形化展示
    :param request:
    :return:
    """
    select = {'day': connection.ops.date_trunc_sql('day', 'create_time')}
    key_data = Report_Results.objects.extra(select=select).values_list('day').annotate(number=Count('id'))
    data_earth = Report_Results.objects.filter(env_Id=4).extra(select=select).values_list('day').annotate(
        number=Count('id'))
    data_moon = Report_Results.objects.filter(env_Id=3).extra(select=select).values_list('day').annotate(
        number=Count('id'))
    date_list = []
    earth_date_list = []
    moon_date_list = []
    earth_list = []
    moon_list = []
    for i in key_data:
        date_list.append(i[0])
    print('x轴日期', date_list)
    for k in data_earth:
        earth_list.append((k[0], k[1]))
    for c in data_moon:
        moon_list.append((c[0], c[1]))
    for m in earth_list:
        earth_date_list.append(m[0])
        less_list = list(set(date_list) - set(earth_date_list))
    for h in moon_list:
        moon_date_list.append(h[0])
        less_list_moon = list(set(date_list) - set(moon_date_list))
    for j in less_list:
        earth_list.append((j, 0))
    for t in less_list_moon:
        moon_list.append((t, 0))
    earth_list.sort(key=takeFirst)
    moon_list.sort(key=takeFirst)
    print('处理后的地球数据', earth_list)
    print('处理后的月亮数据', moon_list)
    json_data = {
        "key": [i[0] for i in key_data],
        "valueEarth": [i[1] for i in earth_list],
        "valueMoon": [i[1] for i in moon_list],
    }
    return JsonResponse(json_data)


def takeFirst(elem):
    """
    list排序指定第一个key
    :param elem:
    :return:
    """
    return elem[0]


def get_data_filter(data_list, all_date):
    """
    数据处理
    :param data_list:
    :param all_date:
    :return:
    """
    date_list = []
    for m in data_list:
        date_list.append(m[0])
        less_list = list(set(all_date) - set(date_list))
    for j in less_list:
        data_list.append((j, 0))
    data_list.sort(key=takeFirst)
    return date_list
