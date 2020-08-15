from login.forms_group import platform_forms
from login.templates.admin.platform.add_Partner.Add_AnchorPartner import add_AnchorPartner
from login.templates.admin.platform.common.Create_Number import create_PhoneNum, create_IDNumber, \
    create_CreditCardNumbers
from login.templates.admin.platform.settlement.get_CurrentTime import month_days
from login.templates.utils.confutils import login_control, init_configs
from django.shortcuts import redirect, render

from login.templates.utils.utils import create_phone


def create_random_num(request):
    """
    生成随机数
    :param request:
    :return:
    """
    if request.session.is_empty() and login_control():
        return redirect('/login/')
    # print('request信息',request.method,request.session.is_empty())
    if request.method:
        Num_form = platform_forms.Create_Num(request.POST)
        if Num_form.is_valid():
            Num_Type = int(Num_form.cleaned_data.get('num_type'))
            print(type(Num_Type))
            print('数据类型：', Num_Type)
            if Num_Type==1:
                phone_num=create_phone()
                print(phone_num)
                message = "生成的手机号为：%s" % (str(phone_num))
            elif Num_Type==2:
                IDNumber=create_IDNumber()
                print(IDNumber)
                message = "生成的身份证号为：%s" % (str(IDNumber))
            else:
                CreditCardNumbers=create_CreditCardNumbers()
                print(CreditCardNumbers)
                message = "生成的银行卡号为：%s" % (str(CreditCardNumbers))
            return render(request, 'login/platform/randomNum.html', locals())
    return render(request, 'login/platform/randomNum.html', locals())