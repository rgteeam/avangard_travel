# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-05 13:50
from __future__ import unicode_literals

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0016_auto_20170805_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='fullticket_store',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.jsonb.JSONField(blank=True), default=[], size=None),
        ),
        migrations.AddField(
            model_name='order',
            name='reduceticket_store',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.jsonb.JSONField(blank=True), default=[], size=None),
        ),
    ]
