# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-06 12:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museums', '0007_auto_20170606_1518'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='max_count',
        ),
        migrations.AddField(
            model_name='schedule',
            name='max_count_full',
            field=models.IntegerField(default=0, verbose_name='Квота билетов взрослых'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='max_count_reduce',
            field=models.IntegerField(default=0, verbose_name='Квота билетов льготных'),
        ),
    ]
