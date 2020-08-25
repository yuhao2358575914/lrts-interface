import os
import urllib

from django.views.decorators.csrf import csrf_exempt
import logging
import re
import requests
import json
from login.run.run_test import run_test_bf_old
from login.templates.utils.confutils import init_configs, login_control, get_services_conf
from login.templates.utils.emails import send_emails, send_emails_multi
from login.templates.utils.getconf import get_conf, write_config_ini
from login.templates.utils.utils import securitycode, geturl, get_local_time_second, getFiles
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from login import models, forms
import time

from login.templates.utils.wechat_robot import msg_robot


def api_test(request):
    """
    懒人api调试
    :param request:
    :return:
    """
    if request.session.is_empty() and login_control():
        return redirect('/login/')
    if request.method:
        requests_form = forms.RequestsForm(request.POST)
        if requests_form.is_valid():
            request_type = requests_form.cleaned_data.get('request_type')
            user_agent = requests_form.cleaned_data.get('user_agent')
            params = requests_form.cleaned_data.get('params')
            host = requests_form.cleaned_data.get('host')
            params = urllib.parse.unquote(params)
            api_name = params.split('?')[0]
            s1 = params.split('?')[1].split('&')
            param_dict = {}
            for i in s1:
                s2 = i.split('=')
                if s2[0] != 'sc':
                    param_dict[s2[0]] = s2[1]
            if request_type == 'post':
                if 'Android' in user_agent:
                    param_dict['sc'] = securitycode(api_name, param_dict)
                    res = requests.post(host + api_name, data=param_dict, headers={'user-agent': user_agent})
                    message = res.text
                    return render(request, 'login/success.html', locals())
                elif 'iOS' in user_agent:
                    param_dict['sc'] = securitycode(api_name, param_dict, 2)
                    res = requests.post(host + api_name, data=param_dict, headers={'user-agent': user_agent})
                    message = res.text
                    return render(request, 'login/success.html', locals())
            elif request_type == 'get':
                if 'Android' in user_agent:
                    param_dict['sc'] = securitycode(api_name, param_dict)
                    res = requests.get(host + api_name + '?' + geturl(param_dict), headers={'user-agent': user_agent})
                    message = res.text
                    return render(request, 'login/success.html', locals())
                elif 'iOS' in user_agent:
                    param_dict['sc'] = securitycode(api_name, param_dict, 2)
                    res = requests.get(host + api_name + '?' + geturl(param_dict), headers={'user-agent': user_agent})
                    message = res.text
                    return render(request, 'login/success.html', locals())
        return render(request, 'login/api_test.html', locals())
    return render(request, 'login/api_test.html', locals())


@csrf_exempt
def run_test(request):
    """
    批量执行用例
    :param request:
    :return:
    """
    # if request.session.is_empty():
    #     return redirect('/login/')
    logger = logging.getLogger('log')
    host_names = 'http://earth-api.mting.info,http://earth-admin.lrts.me'
    test_form = forms.ReportUtils(request.GET)
    if test_form.is_valid():
        envId = test_form.cleaned_data.get('envId')
        if envId == '4':
            host_names = 'http://earth-api.mting.info,http://earth-admin.lrts.me'
        elif envId == '3':
            host_names = 'http://moon-api.mting.info,http://moon-admin.lrts.me'
        elif envId == '5':
            host_names = 'http://mars-api.mting.info,http://mars-admin.lrts.me'
        init_configs(host_names) #修改host和切换数据库
        time.sleep(0.2)
        test_type = test_form.cleaned_data.get('test_type')
        project = test_form.cleaned_data.get('project')
        if test_type == 'All':
            test_type_1 = 'case_*.py'
        elif test_type == 'Nec':
            test_type_1 = 'case_Necessary*.py'
        elif test_type == 'AdminNec':
            test_type_1 = 'case_Necessary_Admin*.py'
        test_results = run_test_bf_old(test_type_1)
        logger.info('测试完成！ 测试结果集合为:{}'.format(test_results))
        file_name = test_results.get('filename')
        test_all = test_results.get('result').get('testAll')
        test_Pass = test_results.get('result').get('testPass')
        test_fail = test_results.get('result').get('testFail')
        test_Error = test_results.get('result').get('testError')
        success_rate = (test_all - test_fail - test_Error) / test_all
        test_results.get('result')['success_rate'] = success_rate
        print('成功率', success_rate)
        data = {
            'envId': envId,
            'test_type': test_type,
            'project': project,
            'successRate': success_rate
        }
        test_repo = models.Report_Results()
        test_repo.reporter_name = file_name
        test_repo.reporter_type = test_type
        test_repo.create_time = get_local_time_second()
        test_repo.publish_module = project
        if request.session.get('user_name'):
            test_repo.create_user = request.session.get('user_name')
        else:
            test_repo.create_user = 'developer'
            # 必测自动发送邮件
            mail_receivers = get_conf('email', 'mail_default_receivers')
            mail_list = mail_receivers.split(',')
            send_emails_multi(mail_list, envId, get_local_time_second(),
                              project, file_name, round(success_rate * 100))
            # 必测自动通知到企业微信群1
            # robotKeys = get_services_conf('keys', 'robotKey')
            robotKeys_earth = get_services_conf('keys', 'robotKeyEarth')
            robotKeys_moon = get_services_conf('keys', 'robotKeyMoon')
            if envId == '4':
                host_name = '地球'
                if ',' in robotKeys_earth:
                    robotKey_list = robotKeys_earth.split(',')
                else:
                    robotKey_list = [robotKeys_earth]
            elif envId == '3':
                host_name = '月亮'
                if ',' in robotKeys_moon:
                    robotKey_list = robotKeys_moon.split(',')
                else:
                    robotKey_list = [robotKeys_moon]
            elif envId == '5':
                host_name = '火星'
            message = {'project': project, 'host_name': host_name, 'test_all': test_all, 'test_Pass': test_Pass,
                       'test_fail': test_fail,
                       'test_Error': test_Error,
                       'success_rate': str(round(success_rate * 100)) + '%',
                       'report_name': file_name}
            for robotKey in robotKey_list:
                msg_robot(message, robotKey)
        test_repo.report_style = '1'
        test_repo.env_Id = envId
        test_repo.report_testAll = test_all
        test_repo.report_testPass = test_Pass
        test_repo.report_testFail = test_fail
        test_repo.report_testError = test_Error
        test_repo.report_successRate = success_rate * 100
        test_repo.save()
        return HttpResponse(json.dumps(data))
        # return render(request, 'login/run_test.html', locals())
    return render(request, 'login/run_test.html', locals())


# def test_report(request):
#     """
#     测试报告
#     :param name:
#     :param request:
#     :return:
#     """
#     # if request.session.is_empty():
#     #     return redirect('/login/')
#     report = models.Report_Results.objects.filter(report_style__exact='1').order_by('-id').values()[0].get(
#         'reporter_name')
#     print('报告名：', report)
#     return render(request, 'login/reports/%s.html' % report, locals())


def test_report(request, report_name):
    """
    测试报告
    :param report_name:
    :param request:
    :return:
    """
    return render(request, 'login/reports/%s.html' % report_name, locals())


def test_report_list10(request):
    """
    返回最近10次测试报告
    :param request:
    :return:
    """
    data = models.Report_Results.objects.filter(report_style__exact='1').order_by('-id').values()[0:10]
    settlement_data = models.settlement_not_vip_models.objects.order_by('create_time').values()[0:10]
    print('结算结果：', settlement_data)
    print('报告列表：', data)
    return render(request,'login/test_report_list10.html', {'data':data,'settlement_data':settlement_data})


def send_email(request):
    """
    邮件发送
    :param request:
    :return:
    """
    if request.session.is_empty() and login_control():
        return redirect('/login/')
    mail_form = forms.SendEmails(request.POST)
    if mail_form.is_valid():
        mail_receivers = mail_form.cleaned_data.get('mail_receivers')
        mail_list = mail_receivers.split(';')
        end_mail_list = []
        for mail in mail_list:
            check = re.compile(r'^\w+@(\w+\.)+(com|cn|net)$')
            if not check.search(mail):
                message = '存在邮箱格式不正确，请检查！'
                return render(request, 'login/send_email.html', locals())
            else:
                end_mail_list.append(mail)
        send_emails(end_mail_list)
    return render(request, 'login/send_email.html', locals())


def run_case(request):
    """
    单条执行用例
    :param request:
    :return:
    """
    if request.session.is_empty() and login_control():
        return redirect('/login/')
    run_id = request.GET.get('run_id')
    print('查询结果：',run_id)
    res = models.TestCases.objects.filter(id=run_id)  # 查看首条数据
    for a in res:
        test_script_name = a.script_name
    abs_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    file_path = abs_path + '\\testcases\cases_ns'
    test_script_name=test_script_name
    exsits=getFiles(file_path,test_script_name)
    if len(exsits)==0:
        response_data="未找到脚本，请检查脚本是否存在！！！"
        return HttpResponse(response_data)
    file_name = run_test_bf_old(test_script_name, run_id)
    obj = models.Report_Results.objects.filter(reporter_type=run_id)
    if obj and len(obj) == 1:#只保存最后一次执行结果
        models.Report_Results.objects.filter(reporter_type=run_id).update(reporter_name=file_name,
                                                                          create_time=get_local_time_second()
                                                                          )
    else:
        test_repo = models.Report_Results()
        test_repo.reporter_name = file_name
        test_repo.reporter_type = run_id
        test_repo.create_time = get_local_time_second()
        if login_control()==False:
            test_repo.create_user='visitor'
        else:
            test_repo.create_user = request.session.get('user_name')
        test_repo.report_style = '2'
        test_repo.save()
    return redirect('/cases_pages/%d' % 1)


def test_report_single(request):
    """
    单条测试报告
    :param name:
    :param request:
    :return:
    """
    if request.session.is_empty() and login_control():
        return redirect('/login/')
    run_id = request.GET.get('run_id') #获取对应url的参数值

    try:  # 尝试执行下列代码
        report = \
            models.Report_Results.objects.filter(report_style__exact='2', reporter_type=run_id).order_by('-id').values()[0].get('reporter_name')
        print('打印一下咯:',type(models.Report_Results.objects.filter(report_style__exact='2', reporter_type=run_id).order_by('-id').values()))
        print(models.Report_Results.objects.filter(report_style__exact='2', reporter_type=run_id).order_by('-id').values())
    except Exception as e:
        print(e)
        return HttpResponse('请先执行用例！！！')
    print('报告名：', report)
    return render(request, 'login/reports/single/%s.html' % report, locals())


def mail_config_manual(request):
    if request.session.is_empty() and login_control():
        return redirect('/login/')
    if request.method == 'POST':
        receivers_new = request.POST.get('receivers')
        if receivers_new == '':
            message = '邮箱配置不能为空！'
            return render(request, 'login/mail_config.html', locals())
        write_config_ini('email', 'mail_default_receivers', receivers_new.strip())
        return redirect('/')
    # 获取配置文件下的收件人邮箱
    receivers = get_conf('email', 'mail_default_receivers')
    if receivers is None:
        receivers = ''
    # 将当前数据渲染到页面上去
    return render(request, 'login/mail_config.html', locals())



