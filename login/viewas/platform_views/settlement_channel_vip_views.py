from login import models
from login.forms_group import platform_forms
from login.templates.admin.platform.settlement.Settlement import Settlement
from login.templates.admin.platform.settlement.SettlementVIP import SettlementVIP, Channel_Settlement
from login.templates.utils.confutils import login_control, init_configs
from django.shortcuts import redirect, render

from login.templates.utils.utils import get_local_time_second


def settlement_channel_vip(request):
    """
    结算非VIP业务
    :param request:
    :return:
    """
    if request.session.is_empty() and login_control():
        return redirect('/login/')
    # print('request信息',request.method,request.session.is_empty())
    if request.method:
        settlement_form = platform_forms.settlement_channel_vip_form(request.POST)
        print('**************',settlement_form)
        print('Settlement_form的类型',type(settlement_form))
        if settlement_form.is_valid():
            Settlement_Date = settlement_form.cleaned_data.get('settlement_date')
            Settlement_Partner_ID = settlement_form.cleaned_data.get('settlement_partner_id')
            PlatformType = int(settlement_form.cleaned_data.get('platformType'))
            if PlatformType==1:
                settlement_record = Channel_Settlement(Settlement_Date,Settlement_Partner_ID).channel_vip_platform_settlement_amount(1)
            else:
                settlement_record = Channel_Settlement(Settlement_Date, Settlement_Partner_ID).channel_vip_platform_settlement_amount(2)
            #从结算结果中取值存表
            results = models.settlement_channel_vip_models()
            results.settlement_month = settlement_record.get('settlement_month')
            results.partner_id = settlement_record.get('partner_id')
            results.can_divide_amount = settlement_record.get('can_divide_amount')
            results.pay_amount = settlement_record.get('pay_amount_in')
            results.divide_baseAmount_final=settlement_record.get('divide_baseAmount_final')
            results.channel_lr_amount=settlement_record.get('channel_lr_amount_in')
            results.settlement_amount=settlement_record.get('settlement_amount')
            results.create_time=get_local_time_second()
            results.update_time=get_local_time_second()
            results.save() #存表操作
            message = "本月实际流水(可分成流水/分成基数)：%s \n" % (settlement_record.get('can_divide_amount')) +\
                      "第三方支付手续费：%s \n" % str(settlement_record.get('pay_amount_in'))+\
                      "合作方分成基数: %s \n" %str(settlement_record.get('divide_baseAmount_final'))+ \
                      "懒人技术服务费: %s \n" % str(settlement_record.get('channel_lr_amount_in'))+ \
                      "分成金额/当月税前: %s \n" % str(settlement_record.get('settlement_amount'))
            return render(request, 'login/platform/settlement_channel_vip.html', locals())
    return render(request, 'login/platform/settlement_channel_vip.html', locals())

def settlement_channel_vip_result(request):
    '''
    结算结果展示
    :param request:
    :return:
    '''
    settlement_data = models.settlement_channel_vip_models.objects.order_by('-create_time').values()[0:10]
    print('结算结果：', settlement_data)
    return render(request, 'login/platform/settlement_channel_vip_result.html', {'settlement_data': settlement_data})