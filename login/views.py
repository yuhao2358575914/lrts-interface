import json
import re

from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
import hashlib
import requests
from login import models, forms
from login.models import IpUtils
from login.run.run_test import run_test_bf_old
from login.templates.admin.account.adminlogin import login_admin
from login.templates.admin.activities.activityBuyShare import add_BuyShare_activity
from login.templates.admin.activities.activityShareListen import add_ShareListen_free_activity
from login.templates.admin.activities.activitySubtract import add_Subtract_activity
from login.templates.admin.activities.send_code import send_ticket_by_exchangeCode, send_vip_by_exchangeCode
from login.templates.admin.book.Book_Operation import get_book_by_pay_type, get_albumn_by_pay_type
from login.templates.config import constant
from login.templates.users.User import check_user_valid, init_register_user_by_phone
from login.templates.utils import utils
from login.templates.utils.confutils import init_configs
from login.templates.utils.emails import send_emails
from login.templates.utils.getconf import write_config_ini, get_config_info
from login.templates.utils.utils import get_local_time_second, securitycode, geturl


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


def api_test(request):
    """
    懒人api调试
    :param request:
    :return:
    """
    if request.session.is_empty():
        return redirect('/login/')
    if request.method:
        requests_form = forms.RequestsForm(request.POST)
        if requests_form.is_valid():
            request_type = requests_form.cleaned_data.get('request_type')
            user_agent = requests_form.cleaned_data.get('user_agent')
            params = requests_form.cleaned_data.get('params')
            host = requests_form.cleaned_data.get('host')
            apiname = params.split('?')[0]
            s1 = params.split('?')[1].split('&')
            param_dict = {}
            for i in s1:
                s2 = i.split('=')
                if s2[0] != 'sc':
                    param_dict[s2[0]] = s2[1]
            if request_type == 'post':
                if 'Android' in user_agent:
                    param_dict['sc'] = securitycode(apiname, param_dict)
                    res = requests.post(host + apiname, data=param_dict, headers={'user-agent': user_agent})
                    message = res.text
                    return render(request, 'login/success.html', locals())
                elif 'iOS' in user_agent:
                    param_dict['sc'] = securitycode(apiname, param_dict, 2)
                    res = requests.post(host + apiname, data=param_dict, headers={'user-agent': user_agent})
                    message = res.text
                    return render(request, 'login/success.html', locals())
            elif request_type == 'get':
                if 'Android' in user_agent:
                    param_dict['sc'] = securitycode(apiname, param_dict)
                    res = requests.get(host + apiname + '?' + geturl(param_dict), headers={'user-agent': user_agent})
                    message = res.text
                    return render(request, 'login/success.html', locals())
                elif 'iOS' in user_agent:
                    param_dict['sc'] = securitycode(apiname, param_dict, 2)
                    res = requests.get(host + apiname + '?' + geturl(param_dict), headers={'user-agent': user_agent})
                    message = res.text
                    return render(request, 'login/success.html', locals())
        return render(request, 'login/api_test.html', locals())
    return render(request, 'login/api_test.html', locals())


def send_code(request):
    """
    根据用户id申请兑换码
    :param request:
    :return:
    """
    if request.session.is_empty():
        return redirect('/login/')
    if request.method:
        send_form = forms.SendCodeForm(request.POST)
        if send_form.is_valid():
            amount = send_form.cleaned_data.get('amount')
            use_scope = send_form.cleaned_data.get('use_scope')
            user_id = send_form.cleaned_data.get('user_id')
            host = send_form.cleaned_data.get('host')
            write_config_ini('HOST', 'apidomain', host.split(',')[0])
            write_config_ini('HOST', 'admindomain', host.split(',')[1])
            if check_user_valid(user_id) == 0:
                message = 'UserID错误！'
                return render(request, 'login/error.html', locals())
            res = send_ticket_by_exchangeCode(amount, user_id, use_scope)
            if res == 0:
                message = '听读券发放成功！'
                new_req = models.SendCode()
                new_req.mount_type = amount
                new_req.exchangeType = use_scope
                new_req.user_id = user_id
                new_req.result = 'success'
                return render(request, 'login/code_success.html', locals())
            else:
                message = '听读券发放失败！'
                new_req = models.SendCode()
                new_req.mount_type = amount
                new_req.exchangeType = use_scope
                new_req.user_id = user_id
                new_req.result = 'fail'
                error(request)
            new_req.save()
    return render(request, 'login/send_code.html', locals())


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


def test_report(request):
    """
    测试报告
    :param request:
    :return:
    """
    if request.session.is_empty():
        return redirect('/login/')
    return render(request, 'login/test_report.html', locals())


def run_test(request):
    """
    执行用例
    :param request:
    :return:
    """
    # if request.session.is_empty():
    #     return redirect('/login/')
    test_form = forms.ReportUtils(request.GET)
    if test_form.is_valid():
        host = test_form.cleaned_data.get('host')
        if host == '1':
            host_names = 'http://earth-api.mting.info,http://earth-admin.lrts.me'
        elif host == '2':
            host_names = 'http://moon-api.mting.info,http://moon-admin.lrts.me'
        elif host == '3':
            host_names = 'http://mars-api.mting.info,http://mars-admin.lrts.me'
        init_configs(host_names)
        test_type = test_form.cleaned_data.get('test_type')
        if test_type == 'All':
            test_type = 'case_*.py'
        elif test_type == 'Nec':
            test_type = 'case_Necessary*.py'
        run_test_bf_old(test_type)
        data = {
            'host': host,
            'test_type': test_type,
            'status': '0',
        }
        return HttpResponse(json.dumps(data))
    return render(request, 'login/run_test.html', locals())


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
    print(request.META)
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


def send_email(request):
    """
    邮件发送
    :param request:
    :return:
    """
    if request.session.is_empty():
        return redirect('/login/')
    mail_form = forms.SendEmails(request.POST)
    if mail_form.is_valid():
        mail_receivers = mail_form.cleaned_data.get('mail_receivers')
        mail_list = mail_receivers.split(';')
        end_mail_list = []
        for mail in mail_list:
            check = re.compile(r'^\w+@(\w+\.)+(com|cn|net)$')
            if not check.search(mail):
                message = '存在邮箱格式不正确，请检查！'
                return render(request, 'login/send_email.html', locals())
            else:
                end_mail_list.append(mail)
        send_emails(end_mail_list)
    return render(request, 'login/send_email.html', locals())


def cases_detail(request):
    """
    用例详情
    :param request:
    :return:
    """
    if request.session.is_empty():
        return redirect('/login/')
    case_list = models.TestCases.objects.all().reverse()
    print(case_list)
    return render(request, 'login/cases_detail.html', locals())


def add_cases(request):
    """
    添加用例
    :param request:
    :return:
    """
    if request.session.is_empty():
        return redirect('/login/')
    if request.method:
        case_form = forms.AddCase(request.POST)
        if case_form.is_valid():
            case_name_ch = case_form.cleaned_data.get('case_name_ch')
            if not case_name_ch:
                message = '请输入用例中文名！'
            case_name_en = case_form.cleaned_data.get('case_name_en')
            if not case_name_en:
                message = '请输入用例英文名！'
            case_steps = case_form.cleaned_data.get('case_steps')
            if not case_steps:
                message = '请输入用例步骤！'
            script_name = case_form.cleaned_data.get('script_name')
            if not script_name:
                message = '请输入python用例脚本名！'
            local_time = get_local_time_second()
            cases = models.TestCases()
            cases.case_name_ch = case_name_ch
            cases.case_name_en = case_name_en
            cases.case_steps = case_steps
            cases.script_name = script_name
            script_name_db = models.TestCases.objects.filter(script_name=script_name)
            if script_name_db:
                message = '该脚本已存在！'
                return render(request, 'login/add_cases.html', locals())
            cases.create_time = local_time
            cases.save()
            redirect('/cases_detail/')
            # return render(request,'login/add_cases.html')
    return render(request, 'login/add_cases.html', locals())


# def edit_case(request):

def delete_case(request):
    """
    删除用例
    :param request:
    :return:
    """
    if request.session.is_empty():
        return redirect('/login/')
    delete_id = request.GET.get('delete_id')
    print(delete_id)
    res = models.TestCases.objects.filter(id=delete_id).first()  # 查看首条数据
    if res:
        models.TestCases.objects.filter(id=delete_id).delete()  # 删除数据
    return redirect('/cases_detail/')
    return HttpResponse('删除成功')


def run_case(request):
    """
    单条执行用例
    :param request:
    :return:
    """
    if request.session.is_empty():
        return redirect('/login/')
    run_id = request.GET.get('run_id')
    print(run_id)
    res = models.TestCases.objects.filter(id=run_id)  # 查看首条数据
    for a in res:
        test_script_name = a.script_name
    run_test_bf_old(test_script_name)
    return redirect('/cases_detail/')


def case_edit(request):
    """
    编辑用例
    :param request:
    :return:
    """
    if request.session.is_empty():
        return redirect('/login/')
    if request.method == 'POST':
        edit_id = request.POST.get('edit_id')
        case_name_ch = request.POST.get('case_name_ch')
        case_name_en = request.POST.get('case_name_en')
        case_steps = request.POST.get('case_steps')
        script_name = request.POST.get('script_name')
        # 更新数据库
        models.TestCases.objects.filter(id=edit_id).update(case_name_ch=case_name_ch, case_name_en=case_name_en,
                                                           case_steps=case_steps, script_name=script_name)
        return redirect('/cases_detail/')  # 更新完成后重定向页面到查看用例列表页面
    # 获取用户想要修改的用户id
    edit_id = request.GET.get('edit_id')
    # 将该数据查询出来进行渲染
    case_query = models.TestCases.objects.filter(id=int(edit_id)).first()
    print('用例信息：', case_query)
    # 将当前数据渲染到页面上去
    return render(request, 'login/case_edit.html', locals())


def send_vip(request):
    """
    根据用户id赠送vip会员
    :param request:
    :return:
    """
    if request.session.is_empty():
        return redirect('/login/')
    if request.method:
        vip_form = forms.SendVip(request.POST)
        if vip_form.is_valid():
            user_id = vip_form.cleaned_data.get('user_id')
            host = vip_form.cleaned_data.get('host')
            amount = vip_form.cleaned_data.get('amount')
            write_config_ini('HOST', 'apidomain', host.split(',')[0])
            write_config_ini('HOST', 'admindomain', host.split(',')[1])
            if check_user_valid(user_id) == 0:
                message = 'UserID错误！'
                return render(request, 'login/error.html', locals())
            res = send_vip_by_exchangeCode(amount, user_id)
            vip_dict = {'101': '1天', '102': '7天', '103': '15天', '104': '1个月', '105': '3个月', '106': '6个月', '107': '12个月'}
            if res == 1:
                message = '给vip用户%s添加%s成功！' % (user_id, vip_dict[amount])
                return render(request, 'login/success.html', locals())
    return render(request, 'login/send_vip.html', locals())


def vip_expire(request):
    """
    会员过期
    :param request:
    :return:
    """
    if request.session.is_empty():
        return redirect('/login/')
    if request.method:
        vipr_form = forms.VipExpire(request.POST)
        if vipr_form.is_valid():
            host_name = vipr_form.cleaned_data.get('host')
            user_id = vipr_form.cleaned_data.get('user_id')
            write_config_ini('HOST', 'apidomain', host_name.split(',')[0])
            write_config_ini('HOST', 'admindomain', host_name.split(',')[1])
            if check_user_valid(user_id) == 0:
                message = 'UserID错误！'
                return render(request, 'login/vip_expire.html', locals())
            r1 = requests.session().get(
                '%s/yytingadmin/tools/subTools?userId=%s&type=4' % (host_name.split(',')[1], user_id),
                cookies={"psid": login_admin()})
            res = json.loads(r1.text)
            if res['status'] == 0:
                message = "用户%sVIP失效成功！" % user_id
                return render(request, 'login/vip_expire.html', locals())
    return render(request, 'login/vip_expire.html', locals())


def add_buy_share(request):
    """
    买一赠一
    :param request:
    :return:
    """
    if request.session.is_empty():
        return redirect('/login/')
    if request.method:
        buy_form = forms.BuyShare(request.POST)
        if buy_form.is_valid():
            host_name = buy_form.cleaned_data.get('host')
            book_num = buy_form.cleaned_data.get('book_num')
            albumn_num = buy_form.cleaned_data.get('albumn_num')
            write_config_ini('HOST', 'apidomain', host_name.split(',')[0])
            write_config_ini('HOST', 'admindomain', host_name.split(',')[1])
            book_ids = get_book_by_pay_type(constant.payType_charge_charpter, int(book_num))
            album_ids = get_albumn_by_pay_type(constant.payType_charge_whole, int(albumn_num))
            avid = add_BuyShare_activity(book_ids, album_ids)
            if avid:
                message = "买一赠一活动成功生成！活动id为：%s" % avid
                return render(request, 'login/add_buy_share.html', locals())
    return render(request, 'login/add_buy_share.html', locals())


def add_ShareListen_free(request):
    """
    分享免费听
    :param request:
    :return:
    """
    if request.session.is_empty():
        return redirect('/login/')
    if request.method:
        share_form = forms.ShareFree(request.POST)
        if share_form.is_valid():
            host_name = share_form.cleaned_data.get('host')
            book_num = share_form.cleaned_data.get('book_num')
            albumn_num = share_form.cleaned_data.get('albumn_num')
            activityId = add_ShareListen_free_activity(
                get_book_by_pay_type(constant.payType_charge_charpter, int(book_num)),
                get_albumn_by_pay_type(constant.payType_charge_whole, int(albumn_num)))
            if activityId:
                message = "分享免费听活动成功生成！活动id为：%s" % activityId
                return render(request, 'login/add_share_listenfree.html', locals())
    return render(request, 'login/add_share_listenfree.html', locals())


def add_Subtracts_activity(request):
    """
    满减
    :param request:
    :return:
    """
    if request.session.is_empty():
        return redirect('/login/')
    if request.method:
        substract_form = forms.SubtractActivity(request.POST)
        if substract_form.is_valid():
            host_name = substract_form.cleaned_data.get('host')
            sub_type = substract_form.cleaned_data.get('sub_type')
            activityId = add_Subtract_activity(sub_type)
            if activityId:
                message = "满减活动成功生成！活动id为：%s" % activityId
                return render(request, 'login/add_substract.html', locals())
    return render(request, 'login/add_substract.html', locals())


def activity_list(request):
    if request.session.is_empty():
        return redirect('/login/')
    return render(request, 'login/activity_init.html', locals())


def init_env(host_name):
    """
    配置修改
    :param host_name:
    :return:
    """
    write_config_ini('HOST', 'apidomain', host_name.split(',')[0])
    write_config_ini('HOST', 'admindomain', host_name.split(',')[1])
