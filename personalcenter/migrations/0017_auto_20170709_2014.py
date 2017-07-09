# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import authwrapper.fields


class Migration(migrations.Migration):

    dependencies = [
        ('personalcenter', '0016_auto_20170709_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='phone',
            field=authwrapper.fields.PhoneNumberNullField(error_messages={'unique': 'A user with that phone number already exists.'}, max_length=30, blank=True, help_text='Required. digits and + only.', unique=True, verbose_name='phone'),
        ),
    ]
