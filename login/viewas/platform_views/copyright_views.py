from login.forms_group import platform_forms
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
            partnerType = copyright_form.cleaned_data.get('partnerType')
            print('数据类型：', type(copyright_type))
            init_configs(host_name)
            copyright_list = []
            for copyright in copyright_type:
                result = add_CopyrightPartner(int(copyright), int(partnerType))
                copyright_list.append(result)
            if copyright_list:
                list_key = [i[0] for i in copyright_list]
                list_value = [i[1] for i in copyright_list]
                print(list_key, list_value)
                json_res = dict(zip(list_key, list_value))
                message = "版权合作方添加成功，列表为：%s" % (str(json_res))
                return render(request, 'login/platform/copyright_partner.html', locals())
    return render(request, 'login/platform/copyright_partner.html', locals())
