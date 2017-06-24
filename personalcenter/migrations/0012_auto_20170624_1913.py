# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personalcenter', '0011_auto_20170624_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='sex',
            field=models.CharField(default=b'male', max_length=30, verbose_name='sex', blank=True, choices=[(b'male', b'Male'), (b'female', b'Female')]),
        ),
    ]
