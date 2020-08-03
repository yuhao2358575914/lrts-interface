# Generated by Django 3.0.8 on 2020-08-03 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='settlement_not_vip_models',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sum_cash_flow', models.CharField(max_length=128)),
                ('sum_cash_flow_billing', models.CharField(max_length=128)),
                ('channel_partner_amount', models.CharField(max_length=128)),
                ('sum_commission_in_original', models.CharField(max_length=128)),
                ('sum_commission_in', models.CharField(max_length=128)),
                ('base_billing_amount_original', models.CharField(max_length=128)),
                ('base_billing_amount', models.CharField(max_length=128)),
                ('partner_amount_original', models.CharField(max_length=128)),
                ('partner_amount', models.CharField(max_length=128)),
                ('tech_amount_original', models.CharField(max_length=128)),
                ('tech_amount', models.CharField(max_length=128)),
                ('baseBillingAounmt_subtract_techAmount_Original', models.CharField(max_length=128)),
                ('baseBillingAounmt_subtract_techAmount', models.CharField(max_length=128)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField()),
            ],
            options={
                'verbose_name': '非VIP会员业务结算结果',
            },
        ),
    ]
