# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-28 20:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('museums', '0013_auto_20170710_1951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='start_time',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='Начало'),
        ),
    ]
