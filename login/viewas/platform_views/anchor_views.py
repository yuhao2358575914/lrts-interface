from login.formsgroup import platform_forms
from login.templates.admin.platform.add_Partner.Add_ChannelPartner import add_ChannelPartner
from login.templates.utils.confutils import login_control, init_configs
from django.shortcuts import redirect, render


def add_anchor_partner(request):
    """
    添加主播合作方
    :param request:
    :return:
    """
    if request.session.is_empty() and login_control():
        return redirect('/login/')
    if request.method:
        anchor_form = platform_forms.AnchorForm(request.POST)
        if anchor_form.is_valid():
            host_name = anchor_form.cleaned_data.get('host')
            anchor_type = anchor_form.cleaned_data.get('anchor_type')
            print('数据类型：', type(anchor_type))
            init_configs(host_name)
            result = add_ChannelPartner(int(anchor_type))
            if result:
                message = "主播合作方:%s，id为%d添加成功" % (result[1], result[0])
                return render(request, 'login/platform/anchor_partner.html', locals())
    return render(request, 'login/platform/anchor_partner.html', locals())
