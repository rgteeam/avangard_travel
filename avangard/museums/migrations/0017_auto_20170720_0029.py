# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-19 21:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museums', '0016_auto_20170720_0016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='date',
            field=models.DateField(verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='start_time',
            field=models.TimeField(null=True, verbose_name='Начало'),
        ),
    ]
