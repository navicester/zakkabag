# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('inspection', '0010_auto_20170826_1438'),
    ]

    operations = [
        migrations.CreateModel(
            name='extinguisher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name='Name', blank=True)),
                ('capacity', models.CharField(max_length=30, verbose_name='Capacity', blank=True)),
                ('check_person', models.CharField(max_length=30, verbose_name='Check Person', blank=True)),
                ('check_result', models.CharField(max_length=30, verbose_name='Check Result', blank=True)),
                ('check_date', models.DateField(verbose_name='Check Date')),
            ],
        ),
        migrations.CreateModel(
            name='hydrant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accessories', models.CharField(max_length=30, verbose_name='Accessories', blank=True)),
                ('check_person', models.CharField(max_length=30, verbose_name='Check Person', blank=True)),
                ('check_result', models.CharField(max_length=30, verbose_name='Check Result', blank=True)),
                ('check_date', models.DateField(verbose_name='Check Date')),
            ],
        ),
        migrations.CreateModel(
            name='rehearsal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField(max_length=30, verbose_name='Title', blank=True)),
                ('date', models.DateField(verbose_name='Date')),
                ('attachment', models.FileField(upload_to=b'', verbose_name='Attachment', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='shelf_annual_inspection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(verbose_name='Annual Inspection Date')),
                ('next_date', models.DateField(verbose_name='Next Inspection Date')),
            ],
        ),
        migrations.CreateModel(
            name='shelf_annual_inspection_image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'inspection/shelf_annual_inspection', null=True, verbose_name='image', blank=True)),
                ('shelf_annual_inspection', models.ForeignKey(to='inspection.shelf_annual_inspection')),
            ],
        ),
        migrations.AddField(
            model_name='shelf_inspection_record',
            name='forecast_complete_time',
            field=models.DateField(default=datetime.datetime(2017, 8, 26, 7, 28, 54, 98000, tzinfo=utc), verbose_name='Forecast Complete Time'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shelf',
            name='compartment',
            field=models.CharField(max_length=30, verbose_name='Compartment Number', blank=True),
        ),
        migrations.AlterField(
            model_name='shelf',
            name='group',
            field=models.CharField(max_length=30, verbose_name='Shelf Group', blank=True),
        ),
        migrations.AlterField(
            model_name='shelf',
            name='number',
            field=models.CharField(max_length=30, verbose_name='Warehouse Number', blank=True),
        ),
        migrations.AlterField(
            model_name='shelf',
            name='type',
            field=models.CharField(max_length=30, verbose_name='Shelf Type', blank=True),
        ),
        migrations.AlterField(
            model_name='shelf',
            name='warehouse',
            field=models.CharField(max_length=30, verbose_name='Warehouse Number', blank=True),
        ),
        migrations.AlterField(
            model_name='shelf',
            name='warehouse_channel',
            field=models.CharField(max_length=30, verbose_name='Warehouse Channel Number', blank=True),
        ),
        migrations.AlterField(
            model_name='shelf_inspection_record',
            name='use_condition',
            field=models.CharField(blank=True, max_length=30, verbose_name='Use Condition', choices=[(b'1', 'Normal'), (b'2', 'Breakdown')]),
        ),
    ]
