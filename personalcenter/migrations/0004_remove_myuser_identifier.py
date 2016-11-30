# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personalcenter', '0003_auto_20161127_2140'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='identifier',
        ),
    ]
