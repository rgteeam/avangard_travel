# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-05 13:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_auto_20170805_1619'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='fullticket_store',
        ),
        migrations.RemoveField(
            model_name='order',
            name='reduceticket_store',
        ),
    ]