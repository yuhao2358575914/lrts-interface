from login import models
from login.forms_group import platform_forms
from login.templates.admin.platform.settlement.Settlement import Settlement
from login.templates.admin.platform.settlement.SettlementVIP import SettlementVIP
from login.templates.utils.confutils import login_control, init_configs
from django.shortcuts import redirect, render

from login.templates.utils.utils import get_local_time_second


def settlement_vip(request):
    """
    结算非VIP业务
    :param request:
    :return:
    """
    if request.session.is_empty() and login_control():
        return redirect('/login/')
    # print('request信息',request.method,request.session.is_empty())
    if request.method:
        settlement_form = platform_forms.settlement_vip_form(request.POST)
        print('**************',settlement_form)
        print('Settlement_form的类型',type(settlement_form))
        if settlement_form.is_valid():
            Settlement_Date = settlement_form.cleaned_data.get('settlement_date')
            Settlement_Res_ID = settlement_form.cleaned_data.get('settlement_res_id')
            PlatformType=int(settlement_form.cleaned_data.get('platformType'))
            print('懒人听书----------------------',PlatformType)
            Settlement_Partner_ID = settlement_form.cleaned_data.get('settlement_partner_id')
            Settlement_Partner_Rate = settlement_form.cleaned_data.get('settlement_partner_rate')
            if PlatformType==1:
                settlement_record = SettlementVIP(Settlement_Date,Settlement_Res_ID,Settlement_Partner_ID,Settlement_Partner_Rate).platform_book_settlement_amount(1)
            else:
                settlement_record = SettlementVIP(Settlement_Date, Settlement_Res_ID, Settlement_Partner_ID,Settlement_Partner_Rate).platform_book_settlement_amount(2)
            #从结算结果中取值存表
            results = models.settlement_vip_models()
            results.settlement_month = settlement_record.get('settlement_month')
            results.partner_id = settlement_record.get('partner_id')
            results.entity_id = settlement_record.get('entity_id')
            results.sum_cash_flow = settlement_record.get('book_platform_amount_final')
            results.book_playCount=settlement_record.get('book_playCount')
            results.partner_divide_rate=settlement_record.get('partner_divide_rate')
            results.partner_divide_money_final=settlement_record.get('partner_divide_money_final')
            results.tech_service_consumption=settlement_record.get('tech_service_consumption')
            results.create_time=get_local_time_second()
            results.update_time=get_local_time_second()
            results.save() #存表操作
            message = "本月实际流水(可分成流水/分成基数)：%s \n" % (settlement_record.get('book_platform_amount_final')) +\
                      "书籍有效播放次数：%s \n" % str(settlement_record.get('book_playCount'))+\
                      "分成比例: %s \n" %str(settlement_record.get('partner_divide_rate'))+ \
                      "分成金额: %s \n" % str(settlement_record.get('partner_divide_money_final'))+ \
                      "懒人技术服务费: %s \n" % str(settlement_record.get('tech_service_consumption'))
            return render(request, 'login/platform/settlement_vip.html', locals())
    return render(request, 'login/platform/settlement_vip.html', locals())

def settlement_vip_result(request):
    '''
    结算结果展示
    :param request:
    :return:
    '''
    settlement_data = models.settlement_vip_models.objects.order_by('-create_time').values()[0:10]
    print('结算结果：', settlement_data)
    return render(request, 'login/platform/settlement_vip_result.html', {'settlement_data': settlement_data})