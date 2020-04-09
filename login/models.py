from django.db import models


class User(models.Model):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default="男")
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
    case_name_ch = models.CharField(max_length=64)
    case_name_en = models.CharField(max_length=64)
    case_steps = models.CharField(max_length=128)
    script_name = models.CharField(max_length=64)
    create_time = models.DateTimeField(auto_now_add=True)
