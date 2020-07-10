from login.forms import platform_forms
from login.templates.admin.platform.add_Partner.Add_CopyrightPartner import add_CopyrightPartner
from login.templates.utils.confutils import login_control, init_configs
from django.shortcuts import redirect, render


def add_copyright_partner(request):
    """
    添加版权合作方
    :param request:
    :return:
    """
    if request.session.is_empty() and login_control():
        return redirect('/login/')
    if request.method:
        copyright_form = platform_forms.CopyrightForm(request.POST)
        if copyright_form.is_valid():
            host_name = copyright_form.cleaned_data.get('host')
            copyright_type = copyright_form.cleaned_data.get('copyright_type')
            print('数据类型：', type(copyright_type))
            init_configs(host_name)
            result = add_CopyrightPartner(int(copyright_type))
            if result:
                message = "版权合作方:%s，id为%d添加成功" % (result[1], result[0])
                return render(request, 'login/platform/copyright_partner.html', locals())
    return render(request, 'login/platform/copyright_partner.html', locals())
