# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('personalcenter', '0004_remove_myuser_identifier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wechatuserprofile',
            name='user',
            field=models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
