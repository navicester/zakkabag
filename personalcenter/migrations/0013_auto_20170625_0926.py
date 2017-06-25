# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('personalcenter', '0012_auto_20170624_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='phone',
            field=models.CharField(validators=[django.core.validators.RegexValidator(b'^(130|131|132|133|134|135|136|137|138|139)\\d{8}$', 'Enter a valid phone number. This value may contain only numbers and /+ characters.', b'invalid')], error_messages={b'unique': 'A user with that phone number already exists.'}, max_length=30, blank=True, help_text='Required. digits and /+ only.', unique=True, verbose_name='phone'),
        ),
    ]
