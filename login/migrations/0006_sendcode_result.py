# Generated by Django 2.0.2 on 2019-12-24 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_auto_20191224_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='sendcode',
            name='result',
            field=models.CharField(default=0, max_length=32),
            preserve_default=False,
        ),
    ]
