import django.utils.timezone as timezone

from django.db import models


class User(models.Model):
    p_type = (
        ('1', "管理员"),
        ('2', "普通用户"),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=32, choices=p_type, default="2")
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"


class Requests(models.Model):
    method_ty = (
        ('post', 'POST'),
        ('get', 'GET')
    )
    method_type = models.CharField(max_length=64, choices=method_ty, default="GET")
    header = models.CharField(max_length=256)
    params = models.CharField(max_length=1024)
    apiname = models.CharField(max_length=256)
    host = models.CharField(max_length=1024)
    result = models.CharField(max_length=1024)

    def __str__(self):
        return self.apiname

    class Meta:
        ordering = ["id"]
        verbose_name = "接口请求"
        verbose_name_plural = "接口请求"


class SendCode(models.Model):
    """
    听读券赠送表
    """
    mount_type = models.CharField(max_length=64)
    user_id = models.CharField(max_length=64)
    exchangeType = models.CharField(max_length=64)
    result = models.CharField(max_length=32)
    send_time = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "兑换码"
        verbose_name_plural = "兑换码"


class IpUtils(models.Model):
    ip = models.CharField(max_length=64)
    login_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "登录用户ip获取"
        verbose_name_plural = "登录用户ip获取"


class TestCases(models.Model):
    status_choices = (
        ('1', '已实现'),
        ('2', '未实现'),
    )
    case_name_ch = models.CharField(max_length=64)
    case_name_en = models.CharField(max_length=64)
    case_steps = models.CharField(max_length=128)
    script_name = models.CharField(max_length=64)
    create_time = models.DateTimeField(auto_now_add=True)
    case_creater = models.CharField(max_length=64, default='lazy')

    # case_status = models.CharField(max_length=8, choices=status_choices, default="2")

    class Meta:
        verbose_name = "测试用例"
        verbose_name_plural = "测试用例"


class Report_Results(models.Model):
    type = (
        ('All', "全量用例"),
        ('Nec', "必测用例"),
        ('Single', "单条用例")
    )
    style = (
        ('1', '批量执行'),
        ('2', '单条执行'),
    )
    reporter_name = models.CharField(max_length=164)
    reporter_type = models.CharField(max_length=32, choices=type, default="全量用例") #Nec-必测用例批量执行;All-全量用例批量执行;数字-单条用例执行的用例id
    create_user = models.CharField(max_length=64)
    create_time = models.DateTimeField(auto_now_add=True)
    report_style = models.CharField(max_length=8, choices=style, default="1") #报告类型，1批量执行 2单条执行
    env_Id = models.CharField(max_length=8, default='4') #host类型，4-地球，3-月亮，5-火星
    report_testAll = models.IntegerField(default=0) #批量执行的总用例数
    report_testPass = models.IntegerField(default=0)#批量执行的通过用例数
    report_testFail = models.IntegerField(default=0)#批量执行的失败用例数
    report_testError = models.IntegerField(default=0)#批量执行的错误用例数
    report_successRate = models.IntegerField(default=0)#批量执行的通过率
    publish_module = models.CharField(max_length=64, default="yyting-apps-api")#批量执行对应的后台api模块

    class Meta:
        verbose_name = "测试报告"
        verbose_name_plural = "测试报告"



class AutoTest_Results(models.Model):
    script_name = models.CharField(max_length=164)
    test_response = models.CharField(max_length=2048)
    test_result = models.CharField(max_length=8)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField()
    tester = models.CharField(max_length=64)
    class Meta:
        verbose_name = "测试结果"
        verbose_name_plural = "测试结果"

class settlement_not_vip_models(models.Model):
    '''结算非VIP会员业务models类'''
    settlement_month=models.CharField(max_length=32,default='Null')
    partner_id=models.CharField(max_length=32,default='Null')
    entity_id=models.CharField(max_length=32,default='Null')
    business=models.CharField(max_length=32,default='Null')
    sum_cash_flow = models.CharField(max_length=64)
    sum_cash_flow_billing = models.CharField(max_length=64)
    channel_partner_amount = models.CharField(max_length=64)
    sum_commission_in=models.CharField(max_length=64)
    base_billing_amount=models.CharField(max_length=64)
    partner_amount=models.CharField(max_length=64)
    tech_amount=models.CharField(max_length=64)
    baseBillingAounmt_subtract_techAmount=models.CharField(max_length=64)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField()
    class Meta:
        verbose_name = "非VIP会员业务结算结果"

class settlement_vip_models(models.Model):
    '''结算VIP会员业务models类'''
    sum_cash_flow = models.CharField(max_length=64)
    book_playCount = models.CharField(max_length=64)
    partner_divide_rate = models.CharField(max_length=64)
    partner_divide_money_final=models.CharField(max_length=64)
    tech_service_consumption=models.CharField(max_length=64)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField()
    class Meta:
        verbose_name = "VIP会员业务结算结果"




# class AutoTest_Results_T(models.Model):
#     script_name = models.CharField(max_length=164)
#     test_response = models.CharField(max_length=2048)
#     test_result = models.CharField(max_length=8)
#     create_time = models.DateTimeField(auto_now_add=True)
#     update_time = models.DateTimeField()
#     tester = models.CharField(max_length=64)
#     class Meta:
#         verbose_name = "测试结果"
#         verbose_name_plural = "测试结果"
# class Devices_Management(models.Model):
#     device_type=models.CharField(max_length=32)
#     device_logo = models.CharField(max_length=32)
#     device_version = models.CharField(max_length=64)
#     device_operation_system = models.CharField(max_length=64)
#     device_defi = models.CharField(max_length=64)
