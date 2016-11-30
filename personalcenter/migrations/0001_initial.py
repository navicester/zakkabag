# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('identifier', models.CharField(unique=True, max_length=50, db_index=True)),
                ('account_type', models.CharField(default=b'username', max_length=50, null=True, blank=True, choices=[(b'username', b'Username'), (b'mail', b'Mail'), (b'wechat', b'Wechat'), (b'phone', b'Phone')])),
                ('nickname', models.CharField(max_length=120, null=True, blank=True)),
                ('sex', models.CharField(max_length=45, null=True, blank=True)),
                ('city', models.CharField(max_length=45, null=True, blank=True)),
                ('country', models.CharField(max_length=45, null=True, blank=True)),
                ('language', models.CharField(max_length=45, null=True, blank=True)),
                ('is_active', models.BooleanField(default=True, verbose_name=b'active')),
                ('is_staff', models.BooleanField(default=True, verbose_name=b'staff')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WechatUserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('openid', models.CharField(max_length=120, null=True, blank=True)),
                ('unionid', models.CharField(max_length=120, null=True, blank=True)),
                ('privilege', models.CharField(max_length=120, null=True, blank=True)),
                ('headimgurl', models.CharField(max_length=120, null=True, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
