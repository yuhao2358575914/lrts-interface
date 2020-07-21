import os
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from login import models
from login import forms
from django.db.models import Q
import pandas as pd
from login.templates.utils.confutils import login_control
from login.templates.utils.utils import get_local_time_second


def cases_detail(request):
    """
    用例详情
    :param request:
    :return:
    """
    if request.session.is_empty() and login_control():
        return redirect('/login/')
    case_list = models.TestCases.objects.all().reverse()
    return render(request, 'login/cases_detail.html', locals())


def cases_pages(request, pindex):
    """
    用例集-分页展示

    """
    if request.session.is_empty() and login_control():
        return redirect('/login/')
    case_obj = models.TestCases.objects.all()
    case_list = []
    for i in case_obj:
        case_list.append(i)
    paginator = Paginator(case_list, 15)
    if pindex == "":
        pindex = 1
    else:  # 如果有返回值，把返回值转为整数型
        int(pindex)
    page = paginator.page(pindex)
    strat = (int(pindex) - 1) * 15
    context = {"page": page, "strat": strat}
    return render(request, "login/cases_pages.html", context)


def search_case(request):
    """
    用例查询
    :param request:
    :return:
    """
    if request.session.is_empty() and login_control():
        return redirect('/login/')
    query = request.GET.get('query')
    if not query:
        return redirect('/cases_pages/%d' % 1)
    case_list = models.TestCases.objects.filter(Q(script_name__icontains=query.strip()))
    print('查询结果', case_list)
    return render(request, 'login/cases_detail.html', locals())


def upload_cases(request):
    if request.session.is_empty() and login_control():
        return redirect('/login/')
    if request.method == 'POST':
        File = request.FILES.get('files_excel', None)
        if File is None:
            return HttpResponse("请选择需要上传的文件")
        else:
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/files'
            f = open(os.path.join(BASE_DIR, File.name), 'wb')
            for chunk in File.chunks():
                f.write(chunk)
            f.close()
            excel_type = f.name.split('.')[-1]
            if excel_type in ['xlsx', 'xls', 'csv']:
                data = pd.read_excel(f.name, sheet_name=0)
                row_count = data.shape[0]
                if row_count < 1:
                    return HttpResponse("无可导入用例，请检查！")
                local_time = get_local_time_second()
                for row in range(row_count):
                    row_data = data.loc[row]
                    cases = models.TestCases()
                    cases.case_name_ch = row_data[0]
                    cases.case_name_en = row_data[1]
                    cases.case_steps = row_data[2]
                    cases.script_name = row_data[3]
                    cases.case_creater = row_data[4]
                    script_name_db = models.TestCases.objects.filter(script_name=row_data[3])
                    cases.create_time = local_time
                    if not script_name_db:
                        cases.save()  # 判断去重，新增用例则写入数据库
                return redirect('/cases_detail/')
            else:
                return HttpResponse("文件格式不正确")
    else:
        return render(request, 'login/cases_pages/%d.html' % 1, locals())


def add_cases(request):
    """
    添加用例
    :param request:
    :return:
    """
    if request.session.is_empty() and login_control():
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
            cases.case_creater = request.session.get('user_name')
            cases.save()
            redirect('/cases_detail/')
    return render(request, 'login/add_cases.html', locals())


def delete_case(request):
    """
    删除用例
    :param request:
    :return:
    """
    if request.session.is_empty() and login_control():
        return redirect('/login/')
    delete_id = request.GET.get('delete_id')
    print(delete_id)
    res = models.TestCases.objects.filter(id=delete_id).first()  # 查看首条数据
    if res:
        models.TestCases.objects.filter(id=delete_id).delete()  # 删除数据
    return redirect('/cases_pages/%d' % 1)
    # return HttpResponse('删除成功')


def case_edit(request):
    """
    编辑用例
    :param request:
    :return:
    """
    if request.session.is_empty() and login_control():
        return redirect('/login/')
    if request.method == 'POST':
        edit_id = request.POST.get('edit_id')
        case_name_ch = request.POST.get('case_name_ch')
        case_name_en = request.POST.get('case_name_en')
        case_steps = request.POST.get('case_steps')
        script_name = request.POST.get('script_name')
        update_user = request.session.get('user_name')
        # 更新数据库
        models.TestCases.objects.filter(id=edit_id).update(case_name_ch=case_name_ch, case_name_en=case_name_en,
                                                           case_steps=case_steps, script_name=script_name,
                                                           case_creater=update_user)
        return redirect('/cases_pages/%d' % 1)  # 更新完成后重定向页面到查看用例列表页面
    # 获取用户想要修改的用户id
    edit_id = request.GET.get('edit_id')
    # 将该数据查询出来进行渲染
    case_query = models.TestCases.objects.filter(id=int(edit_id)).first()
    print('用例信息：', case_query)
    # 将当前数据渲染到页面上去
    return render(request, 'login/case_edit.html', locals())
