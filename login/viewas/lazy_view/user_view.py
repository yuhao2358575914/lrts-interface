from django.shortcuts import redirect, render

import time
import requests
import json
from login.templates.admin.account.adminlogin import login_admin
from login.templates.admin.account.user_account import charge_coin_to_user
from login.templates.admin.activities.send_code import send_vip_by_exchangeCode, send_ticket_by_exchangeCode
from login.templates.users.User import check_user_valid
from login.templates.utils.confutils import init_configs, login_control
from login import models, forms
from login.templates.utils.utils import get_local_time_second


def send_vip(request):
    """
    根据用户id赠送vip会员
    :param request:
    :return:
    """
    if request.session.is_empty() and login_control():
        return redirect('/login/')
    if request.method:
        vip_form = forms.SendVip(request.POST)
        if vip_form.is_valid():
            user_id = vip_form.cleaned_data.get('user_id')
            host_name = vip_form.cleaned_data.get('host')
            amount = vip_form.cleaned_data.get('amount')
            init_configs(host_name)
            time.sleep(0.2)
            if check_user_valid(user_id) == 0:
                message = 'UserID错误！'
                return render(request, 'login/send_vip.html', locals())
            res = send_vip_by_exchangeCode(amount, user_id)
            vip_dict = {'101': '1天', '102': '7天', '103': '15天', '104': '1个月', '105': '3个月', '106': '6个月', '107': '12个月'}
            if res == 1:
                message = '给vip用户%s添加%s成功！' % (user_id, vip_dict[amount])
                return render(request, 'login/send_vip.html', locals())
            else:
                message = res
                return render(request, 'login/send_vip.html', locals())
    return render(request, 'login/send_vip.html', locals())


def vip_expire(request):
    """
    会员过期
    :param request:
    :return:
    """
    if request.session.is_empty() and login_control():
        return redirect('/login/')
    if request.method:
        vipr_form = forms.VipExpire(request.POST)
        if vipr_form.is_valid():
            host_name = vipr_form.cleaned_data.get('host')
            user_id = vipr_form.cleaned_data.get('user_id')
            init_configs(host_name)
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


def send_code(request):
    """
    根据用户id申请兑换码
    :param request:
    :return:
    """
    if request.session.is_empty() and login_control():
        return redirect('/login/')
    if request.method:
        send_form = forms.SendCodeForm(request.POST)
        if send_form.is_valid():
            amount = send_form.cleaned_data.get('amount')
            use_scope = send_form.cleaned_data.get('use_scope')
            user_id = send_form.cleaned_data.get('user_id')
            host_name = send_form.cleaned_data.get('host')
            print('送券金额：', amount)
            ticket_dict = {'0': '通用', '1': '指定上传者', '10': '指定阅读版权机构', '11': '指定阅读分类', '12': '指定阅读书籍', '20': '指定听书版权机构',
                           '21': '指定有声听书分类', '22': '指定有声书籍', '30': '指定有声节目'}
            init_configs(host_name)
            if check_user_valid(user_id) == 0:
                message = 'UserID错误！'
                return render(request, 'login/error.html', locals())
            for ticket in amount:
                res = send_ticket_by_exchangeCode(ticket, user_id, use_scope)
            local_time = get_local_time_second()
            if res == 0:
                message = '听读券发放成功！'
                new_req = models.SendCode()
                new_req.mount_type = amount
                new_req.exchangeType = use_scope
                new_req.user_id = user_id
                new_req.result = 'success'
                new_req.send_time = local_time
                message = "给用户：{}发送听读券成功！，金额为：{}元，发券类型为：{}".format(user_id, amount, ticket_dict[use_scope])
                return render(request, 'login/send_code.html', locals())
            else:
                message = '听读券发放失败！'
                new_req = models.SendCode()
                new_req.mount_type = amount
                new_req.exchangeType = use_scope
                new_req.user_id = user_id
                new_req.result = 'fail'
                new_req.send_time = local_time
                error(request)
            new_req.save()
            return render(request, 'login/send_code.html', locals())
    return render(request, 'login/send_code.html', locals())


def charge_account(request):
    """
    懒人币充值
    :param request:
    :return:
    """
    if request.session.is_empty() and login_control():
        return redirect('/login/')
    if request.method:
        charge_form = forms.Account_Charge(request.POST)
        if charge_form.is_valid():
            host_name = charge_form.cleaned_data.get('host')
            coin_type = charge_form.cleaned_data.get('coin_type')
            amount = charge_form.cleaned_data.get('amount')
            user_id = charge_form.cleaned_data.get('user_id')
            init_configs(host_name)
            res = charge_coin_to_user(coin_type, amount, user_id)
            if len(amount.split('.')) == 2:
                message = '充值金额必须为整数！'
                return render(request, 'login/charge_account.html', locals())
            if check_user_valid(user_id) == 0:
                message = 'UserID错误！'
                return render(request, 'login/charge_account.html', locals())
            if res == 1:
                message = '充值%s个懒人币成功！' % amount
                return render(request, 'login/charge_account.html', locals())
            else:
                message = res
                return render(request, 'login/charge_account.html', locals())
    return render(request, 'login/charge_account.html', locals())


def error(request):
    return render(request, 'login/error.html')
