# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.core.validators
import personalcenter.models


class Migration(migrations.Migration):

    dependencies = [
        ('personalcenter', '0002_auto_20161127_1857'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='myuser',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterModelManagers(
            name='myuser',
            managers=[
                ('objects', personalcenter.models.MyUserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='city',
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='country',
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='language',
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='nickname',
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='sex',
        ),
        migrations.AddField(
            model_name='myuser',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='email address', blank=True),
        ),
        migrations.AddField(
            model_name='myuser',
            name='first_name',
            field=models.CharField(max_length=30, verbose_name='first name', blank=True),
        ),
        migrations.AddField(
            model_name='myuser',
            name='last_name',
            field=models.CharField(max_length=30, verbose_name='last name', blank=True),
        ),
        migrations.AddField(
            model_name='myuser',
            name='phone',
            field=models.CharField(max_length=30, verbose_name='phone', blank=True),
        ),
        migrations.AddField(
            model_name='myuser',
            name='username',
            field=models.CharField(default='username', error_messages={b'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator(b'^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', b'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wechatuserprofile',
            name='city',
            field=models.CharField(max_length=45, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='wechatuserprofile',
            name='country',
            field=models.CharField(max_length=45, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='wechatuserprofile',
            name='language',
            field=models.CharField(max_length=45, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='wechatuserprofile',
            name='nickname',
            field=models.CharField(max_length=120, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='wechatuserprofile',
            name='sex',
            field=models.CharField(max_length=45, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status'),
        ),
    ]
