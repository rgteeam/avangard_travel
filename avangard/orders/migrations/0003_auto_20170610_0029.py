# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-09 21:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_remove_order_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='chat_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]