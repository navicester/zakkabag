# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import personalcenter.models


class Migration(migrations.Migration):

    dependencies = [
        ('personalcenter', '0006_auto_20161202_2124'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='image',
            field=models.ImageField(default=1, upload_to=personalcenter.models.image_upload_to),
            preserve_default=False,
        ),
    ]
