# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-30 01:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_auto_20170830_0455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatroom',
            name='room_admin',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Admin', to=settings.AUTH_USER_MODEL),
        ),
    ]
