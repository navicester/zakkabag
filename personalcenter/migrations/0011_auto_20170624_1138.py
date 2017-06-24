# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personalcenter', '0010_auto_20170406_2332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='birthday',
            field=models.DateField(null=True, verbose_name='birthday', blank=True),
        ),
    ]
