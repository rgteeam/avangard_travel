# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-17 11:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museums', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField(verbose_name='Начало')),
                ('end_time', models.TimeField(verbose_name='Конец')),
                ('max_count', models.BooleanField(default=False, verbose_name='Квота')),
            ],
        ),
        migrations.AlterField(
            model_name='museum',
            name='accompanying_guide',
            field=models.BooleanField(default=False, verbose_name='Сопровождающий гид'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='audioguide',
            field=models.BooleanField(default=False, verbose_name='Аудиогид'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='max_count',
            field=models.IntegerField(default=0, verbose_name='Квота билетов'),
        ),
        migrations.AlterField(
            model_name='museum',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Название'),
        ),
    ]
