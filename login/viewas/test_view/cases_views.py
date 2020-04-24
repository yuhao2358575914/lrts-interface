from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from login import models, forms
from login import forms
from django.db.models import Q
import json

from login.templates.utils.utils import get_local_time_second


def cases_detail(request):
    """
    用例详情
    :param request:
    :return:
    """
    if request.session.is_empty():
        return redirect('/login/')
    case_list = models.TestCases.objects.all().reverse()
    print(case_list)
    return render(request, 'login/cases_detail.html', locals())


def search_case(request):
    # if request.session.is_empty():
    #     return redirect('/login/')
    query = request.GET.get('query')
    if not query:
        return redirect('/cases_detail/')
    case_list = models.TestCases.objects.filter(Q(script_name__icontains=query))
    print('结果111', case_list)
    return render(request, 'login/cases_detail.html', locals())


def add_cases(request):
    """
    添加用例
    :param request:
    :return:
    """
    if request.session.is_empty():
        return redirect('/login/')
    if request.method:
        case_form = forms.AddCase(request.POST)
        if case_form.is_valid():
            case_name_ch = case_form.cleaned_data.get('case_name_ch')
            if not case_name_ch:
                message = '请输入用例中文名！'
            case_name_en = case_form.cleaned_data.get('case_name_en')
            if not case_name_en:
                message = '请输入用例英文名！'
            case_steps = case_form.cleaned_data.get('case_steps')
            if not case_steps:
                message = '请输入用例步骤！'
            script_name = case_form.cleaned_data.get('script_name')
            if not script_name:
                message = '请输入python用例脚本名！'
            local_time = get_local_time_second()
            cases = models.TestCases()
            cases.case_name_ch = case_name_ch
            cases.case_name_en = case_name_en
            cases.case_steps = case_steps
            cases.script_name = script_name
            script_name_db = models.TestCases.objects.filter(script_name=script_name)
            if script_name_db:
                message = '该脚本已存在！'
                return render(request, 'login/add_cases.html', locals())
            cases.create_time = local_time
            cases.save()
            redirect('/cases_detail/')
            # return render(request,'login/add_cases.html')
    return render(request, 'login/add_cases.html', locals())


# def edit_case(request):

def delete_case(request):
    """
    删除用例
    :param request:
    :return:
    """
    if request.session.is_empty():
        return redirect('/login/')
    delete_id = request.GET.get('delete_id')
    print(delete_id)
    res = models.TestCases.objects.filter(id=delete_id).first()  # 查看首条数据
    if res:
        models.TestCases.objects.filter(id=delete_id).delete()  # 删除数据
    return redirect('/cases_detail/')
    return HttpResponse('删除成功')


def case_edit(request):
    """
    编辑用例
    :param request:
    :return:
    """
    if request.session.is_empty():
        return redirect('/login/')
    if request.method == 'POST':
        edit_id = request.POST.get('edit_id')
        case_name_ch = request.POST.get('case_name_ch')
        case_name_en = request.POST.get('case_name_en')
        case_steps = request.POST.get('case_steps')
        script_name = request.POST.get('script_name')
        # 更新数据库
        models.TestCases.objects.filter(id=edit_id).update(case_name_ch=case_name_ch, case_name_en=case_name_en,
                                                           case_steps=case_steps, script_name=script_name)
        return redirect('/cases_detail/')  # 更新完成后重定向页面到查看用例列表页面
    # 获取用户想要修改的用户id
    edit_id = request.GET.get('edit_id')
    # 将该数据查询出来进行渲染
    case_query = models.TestCases.objects.filter(id=int(edit_id)).first()
    print('用例信息：', case_query)
    # 将当前数据渲染到页面上去
    return render(request, 'login/case_edit.html', locals())
