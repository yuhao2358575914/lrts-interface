from django import forms
from django.forms import CheckboxSelectMultiple,RadioSelect


class CopyrightForm(forms.Form):
    """
    order 0表示勾选全部业务 1表示付费收听 2 表示电子阅读 3表示VIP会员 4 表示漫画
    partnerType 1表示个人账户 2表示公司账户
    """
    host_name = (
        ('http://moon-api.mting.info,http://moon-admin.lrts.me', '月亮'),
    )
    host = forms.ChoiceField(label="测试环境", choices=host_name)
    copyright_choice = (
        (0, '全部业务'),
        (1, '付费收听'),
        (2, '电子阅读'),
        (3, 'VIP会员'),
        (4, '漫画'),
    )
    copyright_type = forms.CharField(label="业务类型", required=False, choices=copyright_choice,
                                               widget=RadioSelect())
    partner_choice = (
        (1, '个人账户'),
        (2, '公司账户'),
    )
    partnerType = forms.ChoiceField(label="账户类型", choices=partner_choice)


class ChannelForm(forms.Form):
    """
    order 0表示勾选全部业务 1表示付费收听 2 表示电子阅读 3 表示主播打赏 4表示VIP会员 5表示漫画
    partnerType 1表示个人账户 2表示公司账户
    """
    host_name = (
        ('http://moon-api.mting.info,http://moon-admin.lrts.me', '月亮'),
    )
    host = forms.ChoiceField(label="测试环境", choices=host_name)
    channel_choice = (
        (0, '全部'),
        (1, '付费收听'),
        (2, '电子阅读'),
        (3, '主播打赏'),
        (4, 'VIP会员'),
        (5, '漫画'),
    )
    channel_type = forms.MultipleChoiceField(label="业务类型", required=False, choices=channel_choice,
                                             widget=CheckboxSelectMultiple())
    partner_choice = (
        (1, '个人账户'),
        (2, '公司账户'),
    )
    partnerType = forms.ChoiceField(label="账户类型", choices=partner_choice)


class AnchorForm(forms.Form):
    """
    order 1表示付费收听 2 表示主播打赏 3 表示VIP会员
    partnerType 1表示个人账户 2表示公司账户
    """
    host_name = (
        ('http://moon-api.mting.info,http://moon-admin.lrts.me', '月亮'),
    )
    host = forms.ChoiceField(label="测试环境", choices=host_name)
    anchor_choice = (
        (1, '付费收听'),
        (2, '主播打赏'),
        (3, 'VIP会员'),
    )
    anchor_type = forms.MultipleChoiceField(label="业务类型", required=False, choices=anchor_choice,
                                            widget=CheckboxSelectMultiple())
    partner_choice = (
        (1, '个人账户'),
        (2, '公司账户'),
    )
    partnerType = forms.ChoiceField(label="账户类型", choices=partner_choice)
