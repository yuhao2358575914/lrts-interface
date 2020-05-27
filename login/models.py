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
    reporter_type = models.CharField(max_length=32, choices=type, default="全量用例")
    create_user = models.CharField(max_length=64)
    create_time = models.DateTimeField(auto_now_add=True)
    report_style = models.CharField(max_length=8, choices=style, default="1")
    env_Id = models.CharField(max_length=8, default='4')
    report_testAll = models.IntegerField(default=0)
    report_testPass = models.IntegerField(default=0)
    report_testFail = models.IntegerField(default=0)
    report_testError = models.IntegerField(default=0)
    report_successRate = models.IntegerField(default=0)

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
