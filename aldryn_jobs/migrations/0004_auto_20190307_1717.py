# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-07 17:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_jobs', '0003_auto_20160714_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapplication',
            name='salutation',
            field=models.CharField(blank=True, max_length=20, verbose_name='salutation'),
        ),
        migrations.AlterField(
            model_name='jobsconfig',
            name='namespace',
            field=models.CharField(default=None, max_length=100, unique=True, verbose_name='Instance namespace'),
        ),
        migrations.AlterField(
            model_name='jobsconfig',
            name='type',
            field=models.CharField(max_length=100, verbose_name='Type'),
        ),
    ]
