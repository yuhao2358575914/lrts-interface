from login import models
from login.formsgroup import platform_forms
from login.templates.admin.platform.settlement.Settlement import Settlement
from login.templates.utils.confutils import login_control, init_configs
from django.shortcuts import redirect, render

from login.templates.utils.utils import get_local_time_second


def settlement_not_vip(request):
    """
    结算非VIP业务
    :param request:
    :return:
    """
    if request.session.is_empty() and login_control():
        return redirect('/login/')
    # print('request信息',request.method,request.session.is_empty())
    if request.method:
        settlement_form = platform_forms.settlement_not_vip_form(request.POST)
        print('**************',settlement_form)
        if settlement_form.is_valid():
            Settlement_Date = settlement_form.cleaned_data.get('settlement_date')
            Settlement_Res_ID = settlement_form.cleaned_data.get('settlement_res_id')
            Settlement_Partner_ID = settlement_form.cleaned_data.get('settlement_partner_id')
            Settlement_Cooperation_Business = settlement_form.cleaned_data.get('settlement_cooperation_business')
            print('数据类型',type(Settlement_Date))
            settlement_record=Settlement(int(Settlement_Date),int(Settlement_Res_ID),int(Settlement_Partner_ID),int(Settlement_Cooperation_Business)).settlement_lr_yaya(1)
            print('数据值：',settlement_record)
            print(type(settlement_record))
            #存表
            results = models.settlement_not_vip_models()
            results.sum_cash_flow = settlement_record.get('lr_sum_cash_flow')
            results.sum_cash_flow_billing=settlement_record.get('lr_sum_cash_flow_billing')
            results.channel_partner_amount=settlement_record.get('lr_channel_partner_amount')
            results.sum_commission_in_original=settlement_record.get('lr_sum_commission_in_original')
            results.sum_commission_in=settlement_record.get('lr_sum_commission_in')
            results.base_billing_amount_original=settlement_record.get('lr_base_billing_amount_original')
            results.base_billing_amount=settlement_record.get('lr_base_billing_amount')
            results.partner_amount_original=settlement_record.get('lr_partner_amount_original')
            results.partner_amount=settlement_record.get('lr_partner_amount')
            results.tech_amount_original=settlement_record.get('lr_tech_amount_original')
            results.tech_amount=settlement_record.get('lr_tech_amount')
            results.baseBillingAounmt_subtract_techAmount_Original=settlement_record.get('baseBillingAounmt_subtract_techAmount_Original')
            results.baseBillingAounmt_subtract_techAmount=settlement_record.get('baseBillingAounmt_subtract_techAmount')
            results.create_time=get_local_time_second()
            results.update_time=get_local_time_second()
            results.save()
            message = "现金：%s \n" % (settlement_record.get('lr_sum_cash_flow')) +\
                      "现金2：%s \n" % str(settlement_record.get('lr_sum_cash_flow_billing'))
            return render(request, 'login/platform/settlement_not_vip.html', locals())
    return render(request, 'login/platform/settlement_not_vip.html', locals())