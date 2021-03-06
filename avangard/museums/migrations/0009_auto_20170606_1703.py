# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-06 14:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('museums', '0008_auto_20170606_1541'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название компании')),
            ],
        ),
        migrations.AddField(
            model_name='schedule',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='museums.Company'),
        ),
    ]
