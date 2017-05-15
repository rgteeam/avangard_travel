# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-14 12:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Museum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('max_count', models.IntegerField(default=0)),
                ('audioguide', models.BooleanField(default=False)),
                ('accompanying_guide', models.BooleanField(default=False)),
            ],
        ),
    ]
