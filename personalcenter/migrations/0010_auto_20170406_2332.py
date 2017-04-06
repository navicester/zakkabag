# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personalcenter', '0009_auto_20170326_1536'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='birthday',
            field=models.DateField(default="1970-01-01", verbose_name='birthday', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='myuser',
            name='nickname',
            field=models.CharField(max_length=30, verbose_name='nickname', blank=True),
        ),
        migrations.AddField(
            model_name='myuser',
            name='sex',
            field=models.CharField(blank=True, max_length=30, verbose_name='sex', choices=[(b'male', b'Male'), (b'female', b'Female')]),
        ),
    ]
