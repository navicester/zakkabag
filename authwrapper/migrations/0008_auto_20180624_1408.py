# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-24 06:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authwrapper', '0007_auto_20180117_2157'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='myuser',
            options={'permissions': (('access_remote', 'access remote'),), 'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterField(
            model_name='myuser',
            name='user_role',
            field=models.CharField(choices=[('admin', 'administrator'), ('staff', 'staff'), ('guest', 'guest')], default='guest', max_length=50, verbose_name='user role'),
        ),
    ]