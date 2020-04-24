from django.shortcuts import render
from django.shortcuts import redirect
import hashlib
from login import models, forms
from login.models import IpUtils

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
            sex = register_form.cleaned_data.get('sex')
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
                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
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
    if request.session.is_empty():
        return redirect('/login/')
    # print(request.session.get('role'))
    # print(request.session.keys())
    # print(request.session.items())
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META.get("HTTP_X_FORWARDED_FOR")
    else:
        ip = request.META.get("REMOTE_ADDR")
    search = IpUtils.objects.filter(ip=ip)
    if not search:
        local_time = get_local_time_second()
        ips = models.IpUtils()
        ips.ip = ip
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
