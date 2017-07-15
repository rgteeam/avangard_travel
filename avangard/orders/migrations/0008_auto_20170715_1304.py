# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-15 10:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_merge_20170711_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
