# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-20 10:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_auto_20170715_1304'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='company',
        ),
    ]
