from django import forms
from django.forms import CheckboxSelectMultiple


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Username", 'autofocus': ''}))
    password = forms.CharField(label="密码", max_length=256,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password"}))
    # captcha = CaptchaField(label='验证码', required=True, error_messages={'required': '验证码不能为空'})


class RegisterForm(forms.Form):
    p_type = (
        ('2', "普通用户"),
        ('1', "管理员"),
    )
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    role = forms.ChoiceField(label="角色", choices=p_type)
    # captcha = CaptchaField(label='验证码', required=True, error_messages={'required': '验证码不能为空'})


class RequestsForm(forms.Form):
    method_ty = (
        ('get', 'GET'),
        ('post', 'POST')
    )
    host_name = (
        ('http://earth-api.mting.info', '地球'),
        ('http://moon-api.mting.info', '月亮'),
        ('http://pm.mting.info', '预发布'),
        ('http://dapi.mting.info', '线上'),
    )
    user_agent = forms.CharField(label="User-Agent", max_length=1024,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control', 'placeholder': "请输入user-agent"}))
    request_type = forms.ChoiceField(label="Method", choices=method_ty)
    params = forms.CharField(label="params", max_length=1024,
                             widget=forms.Textarea(
                                 attrs={'class': 'form-control',
                                        'placeholder': "如：/yyting/userclient/ClientGetUserInfo.action?token=xxx&nwt=xxx..."}))
    host = forms.ChoiceField(label="测试环境", choices=host_name)


class SendCodeForm(forms.Form):
    host_name = (
        ('http://earth-api.mting.info,http://earth-admin.lrts.me', '地球'),
        ('http://moon-api.mting.info,http://moon-admin.lrts.me', '月亮'),
    )
    host = forms.ChoiceField(label="测试环境", choices=host_name)
    ticket_mount = (
        ('1', '面额1元'),
        ('2', '面额2元'),
        ('5', '面额5元'),
        ('10', '面额10元'),
        ('20', '面额20元'),
        ('50', '面额50元'),
        ('100', '面额100元'),
        ('150', '面额150元'),
    )
    ex_type = (
        ('0', '通用'),
        ('1', '指定上传者'),
        ('10', '指定阅读版权机构'),
        ('11', '指定阅读分类'),
        ('12', '指定阅读书籍'),
        ('20', '指定听书版权机构'),
        ('21', '指定有声听书分类'),
        ('22', '指定有声书籍'),
        ('30', '指定有声节目'),
    )

    user_id = forms.CharField(label="用户ID", max_length=64,
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "懒人ID"}))
    # amount = forms.ChoiceField(label="送券面额", choices=ticket_mount)
    amount = forms.MultipleChoiceField(label="送券面额", required=False, widget=CheckboxSelectMultiple(),
                                       choices=ticket_mount)
    use_scope = forms.ChoiceField(label="使用范围", choices=ex_type)


# class CryptUtils(forms.Form):
#     crypt_msg = forms.CharField(label="待加/解密信息", max_length=1024,
#                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
#     crypt_choice = (
#         ('加密', '加密'),
#         ('解密', '解密'),
#     )
#     crypt_type = forms.ChoiceField(label="业务类型", choices=crypt_choice)


class ReportUtils(forms.Form):
    test_choice = (
        ('All', '全量用例'),
        ('Nec', '必测用例'),
        ('AdminNec', 'Admin必测'),
    )
    host_name = (
        ('4', '地球'),
        ('3', '月亮'),
        ('5', '火星'),
    )
    api_choice = (
        ('yyting-apps-api', 'yyting-apps-api'),
        ('yyting-apps-admin','yyting-apps-admin'),
    )
    envId = forms.ChoiceField(label="测试环境", choices=host_name)
    test_type = forms.ChoiceField(label='自动化用例执行类型', choices=test_choice)
    project = forms.ChoiceField(label="Api类型", choices=api_choice,
                                widget=forms.RadioSelect(attrs={'required': 'required',
                                                                'class': 'radioset'}))


class SendEmails(forms.Form):
    mail_receivers = forms.CharField(label="请填写收件人列表:", max_length=1024,
                                     widget=forms.Textarea(
                                         attrs={'class': 'form-control', 'placeholder': "收件人列表以 ; 分隔"}))


class AddCase(forms.Form):
    case_name_ch = forms.CharField(label="用例名-中文", max_length=64,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    case_name_en = forms.CharField(label="用例名-英文", max_length=64,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    case_steps = forms.CharField(label="用例步骤", max_length=64,
                                 widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': "用例步骤"}))
    script_name = forms.CharField(label="脚本名", max_length=64,
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "脚本名，带.py"}))


class SendVip(forms.Form):
    host_name = (
        ('http://earth-api.mting.info,http://earth-admin.lrts.me', '地球'),
        ('http://moon-api.mting.info,http://moon-admin.lrts.me', '月亮'),
    )
    vip_mount = (
        ('101', '一天'),
        ('102', '7天'),
        ('103', '15天'),
        ('104', '1个月'),
        ('105', '3个月'),
        ('106', '6个月'),
        ('107', '12个月'),
    )
    host = forms.ChoiceField(label="测试环境", choices=host_name)

    user_id = forms.CharField(label="用户ID", max_length=64,
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "懒人ID"}))
    amount = forms.ChoiceField(label="赠送VIP金额", choices=vip_mount)


class VipExpire(forms.Form):
    host_name = (
        ('http://earth-api.mting.info,http://earth-admin.lrts.me', '地球'),
        ('http://moon-api.mting.info,http://moon-admin.lrts.me', '月亮'),
    )
    host = forms.ChoiceField(label="测试环境", choices=host_name)
    user_id = forms.CharField(label="用户ID", max_length=64,
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "懒人ID"}))


class BuyShare(forms.Form):
    host_name = (
        ('http://earth-api.mting.info,http://earth-admin.lrts.me', '地球'),
        ('http://moon-api.mting.info,http://moon-admin.lrts.me', '月亮'),
    )
    host = forms.ChoiceField(label="测试环境", choices=host_name)
    book_num = forms.CharField(label="书籍本数", max_length=64,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "请填写正整数"}))
    albumn_num = forms.CharField(label="节目本数", max_length=64,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "请填写正整数"}))


class ShareFree(forms.Form):
    """
    分享免费听
    """
    host_name = (
        ('http://earth-api.mting.info,http://earth-admin.lrts.me', '地球'),
        ('http://moon-api.mting.info,http://moon-admin.lrts.me', '月亮'),
    )
    host = forms.ChoiceField(label="测试环境", choices=host_name)
    book_num = forms.CharField(label="书籍本数", max_length=64,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "请填写正整数"}))
    albumn_num = forms.CharField(label="节目本数", max_length=64,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "请填写正整数"}))


class SubtractActivity(forms.Form):
    """
    满减
    """
    host_name = (
        ('http://earth-api.mting.info,http://earth-admin.lrts.me', '地球'),
        ('http://moon-api.mting.info,http://moon-admin.lrts.me', '月亮'),
    )
    host = forms.ChoiceField(label="测试环境", choices=host_name)
    sub_choice = (
        ('1', '书籍'),
        ('2', '节目'),
        ('3', '阅读'),
    )
    sub_type = forms.ChoiceField(label="满减类型", choices=sub_choice,
                                 widget=forms.RadioSelect(attrs={'required': 'required',
                                                                 'class': 'radioset'}))


class Account_Charge(forms.Form):
    app_type = (
        ('0', '安卓'),
        ('1', 'iOS'),
    )
    host_name = (
        ('http://earth-api.mting.info,http://earth-admin.lrts.me', '地球'),
        ('http://moon-api.mting.info,http://moon-admin.lrts.me', '月亮'),
    )
    host = forms.ChoiceField(label="测试环境", choices=host_name)
    coin_type = forms.ChoiceField(label='懒人币类型', choices=app_type)
    amount = forms.CharField(label='懒人币金额', max_length=64,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "懒人币金额"}))
    user_id = forms.CharField(label='用户ID', max_length=64,
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "懒人ID"}))


class upload_Form(forms.Form):
    introduce = forms.CharField(max_length=50)
    file_path = forms.FileField()


class Case_Search_Form(forms.Form):
    status_choices = (
        ('1', '已实现'),
        ('2', '未实现'),
    )
    case_status = forms.ChoiceField(label='', choices=status_choices)
    search_keyword = forms.CharField(label='2222', max_length=64,
                                     widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "请输入关键字查询"}))


class HostExchange_Form(forms.Form):
    host_choice = (
        ('earth', '地球'),
        ('moon', '月亮'),
        ('mars', '火星'),
    )
    host_value = forms.ChoiceField(label="测试环境切换", choices=host_choice)
