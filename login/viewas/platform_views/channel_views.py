from login.formsgroup import platform_forms
from login.templates.admin.platform.add_Partner.Add_ChannelPartner import add_ChannelPartner
from login.templates.utils.confutils import login_control, init_configs
from django.shortcuts import redirect, render


def add_channel_partner(request):
    """
    添加渠道合作方
    :param request:
    :return:
    """
    if request.session.is_empty() and login_control():
        return redirect('/login/')
    if request.method:
        channel_form = platform_forms.ChannelForm(request.POST)
        if channel_form.is_valid():
            host_name = channel_form.cleaned_data.get('host')
            channel_type = channel_form.cleaned_data.get('channel_type')
            partnerType = channel_form.cleaned_data.get('partnerType')
            print('数据类型：', type(channel_type))
            init_configs(host_name)
            result = add_ChannelPartner(int(channel_type), int(partnerType))
            if result:
                message = "渠道合作方:%s，id为%d添加成功" % (result[1], result[0])
                return render(request, 'login/platform/channel_partner.html', locals())
    return render(request, 'login/platform/channel_partner.html', locals())
