import json

from login.forms_group import platform_forms
from login.templates.admin.platform.add_Partner.Add_ChannelPartner import add_ChannelPartner
from login.templates.admin.platform.channel_manage.developer_manage import add_channel_by_type, approve_channel_by_id
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
            channel_list = []
            for channel in channel_type:
                result = add_ChannelPartner(int(channel), int(partnerType))
                channel_list.append(result)
            if channel_list:
                list_key = [i[0] for i in channel_list]
                list_value = [i[1] for i in channel_list]
                print(list_key, list_value)
                json_res = dict(zip(list_key, list_value))
                message = "渠道合作方添加成功，列表为：%s" % (str(json_res))
                return render(request, 'login/platform/channel_partner.html', locals())
    return render(request, 'login/platform/channel_partner.html', locals())


def add_develop_channel(request):
    """
    添加开发者
    :param request:
    :return:
    """
    if request.session.is_empty() and login_control():
        return redirect('/login/')
    if request.method:
        channel = platform_forms.DevelopChannelForm(request.POST)
        if channel.is_valid():
            host_name = channel.cleaned_data.get('host')
            channel_type = channel.cleaned_data.get('channel_type')
            approve_Type = channel.cleaned_data.get('approveType')
            print('数据类型：', type(channel_type))
            init_configs(host_name)
            channel_list = []
            if approve_Type == '1':
                channel_info = add_channel_by_type(channel_type)
                result = approve_channel_by_id(channel_info['id'])
                message = "开发者添加成功，信息为：%s，已审核通过！" % (str(result))
            elif approve_Type == '2':
                result = add_channel_by_type(channel_type)
                message = "开发者添加成功，信息为：%s，未审核！" % (str(result))
            return render(request, 'login/platform/channel_developer.html', locals())
    return render(request, 'login/platform/channel_developer.html', locals())
