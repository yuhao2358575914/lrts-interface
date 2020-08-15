from login.forms_group import platform_forms
from login.templates.admin.platform.add_Partner.Add_AnchorPartner import add_AnchorPartner
from login.templates.admin.platform.settlement.get_CurrentTime import month_days
from login.templates.utils.confutils import login_control, init_configs
from django.shortcuts import redirect, render


def month_day(request):
    """
    获取当前月份的天数
    :param request:
    :return:
    """
    if request.session.is_empty() and login_control():
        return redirect('/login/')
    # print('request信息',request.method,request.session.is_empty())
    if request.method:
        print('******************')
        month_days_form = platform_forms.Month_Days(request.POST)
        if month_days_form.is_valid():
            month_days_name = month_days_form.cleaned_data.get('month_days')
            print('数据类型：', type(month_days_name))
            days=month_days(month_days_name)
            message = "当前月份的天数为：%s" % (str(days))
            return render(request, 'login/platform/dates.html', locals())
    return render(request, 'login/platform/dates.html', locals())