# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personalcenter', '0005_auto_20161202_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wechatuserprofile',
            name='headimgurl',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
    ]
