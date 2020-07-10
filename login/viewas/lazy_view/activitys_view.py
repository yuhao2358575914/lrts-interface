from django.shortcuts import redirect, render

from login import forms
from login.templates.admin.activities.activityBuyShare import add_BuyShare_activity
from login.templates.admin.activities.activityShareListen import add_ShareListen_free_activity
from login.templates.admin.activities.activitySubtract import add_Subtract_activity
from login.templates.admin.book.Book_Operation import get_book_by_pay_type, get_albumn_by_pay_type
from login.templates.utils.confutils import init_configs, login_control
from login.templates.config import constant


def add_buy_share(request):
    """
    买一赠一
    :param request:
    :return:
    """
    if request.session.is_empty() and login_control():
        return redirect('/login/')
    if request.method:
        buy_form = forms.BuyShare(request.POST)
        if buy_form.is_valid():
            host_name = buy_form.cleaned_data.get('host')
            book_num = buy_form.cleaned_data.get('book_num')
            albumn_num = buy_form.cleaned_data.get('albumn_num')
            init_configs(host_name)
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
    if request.session.is_empty() and login_control():
        return redirect('/login/')
    if request.method:
        share_form = forms.ShareFree(request.POST)
        if share_form.is_valid():
            host_name = share_form.cleaned_data.get('host')
            book_num = share_form.cleaned_data.get('book_num')
            albumn_num = share_form.cleaned_data.get('albumn_num')
            init_configs(host_name)
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
    if request.session.is_empty() and login_control():
        return redirect('/login/')
    if request.method:
        substract_form = forms.SubtractActivity(request.POST)
        if substract_form.is_valid():
            host_name = substract_form.cleaned_data.get('host')
            sub_type = substract_form.cleaned_data.get('sub_type')
            init_configs(host_name)
            activityId = add_Subtract_activity(sub_type)
            if activityId:
                message = "满减活动成功生成！活动id为：%s" % activityId
                return render(request, 'login/add_substract.html', locals())
    return render(request, 'login/add_substract.html', locals())


def items_list(request, x_type):
    if request.session.is_empty() and login_control():
        return redirect('/login/')
    if x_type == "1":
        return render(request, 'login/activity_init.html', locals())
    elif x_type == "2":
        return render(request, 'login/platform/platform_all.html', locals())