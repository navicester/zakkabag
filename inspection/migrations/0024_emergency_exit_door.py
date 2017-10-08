# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-10-08 01:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspection', '0023_auto_20171006_1431'),
    ]

    operations = [
        migrations.CreateModel(
            name='emergency_exit_door',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=30, verbose_name='Location')),
                ('use_condition', models.CharField(default=b'normal', max_length=30, verbose_name='Use Condition')),
                ('inspector', models.CharField(max_length=30, verbose_name='Inspector')),
                ('date_of_inspection', models.DateTimeField(auto_now=True, verbose_name='Date of Inspection')),
            ],
        ),
    ]
