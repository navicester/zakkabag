# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import authwrapper.fields
import authwrapper.validators


class Migration(migrations.Migration):

    dependencies = [
        ('personalcenter', '0014_auto_20170625_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='email',
            field=authwrapper.fields.EmailNullField(max_length=255, unique=True, null=True, verbose_name='email address', blank=True),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='phone',
            field=authwrapper.fields.PhoneNumberNullField(validators=[django.core.validators.RegexValidator('^(130|131|132|133|134|135|136|137|138|139)\\d{8}$', 'Enter a valid phone number. This value may contain only numbers and + characters.', 'invalid')], error_messages={'unique': 'A user with that phone number already exists.'}, max_length=30, blank=True, help_text='Required. digits and + only.', unique=True, verbose_name='phone'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=30, validators=[authwrapper.validators.ASCIIUsernameValidator()], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username'),
        ),
    ]
