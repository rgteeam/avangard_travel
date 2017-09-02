# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-30 09:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0010_remove_chatroom_room_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='room_admin',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Admin', to=settings.AUTH_USER_MODEL),
        ),
    ]