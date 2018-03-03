# Generated by Django 2.0.2 on 2018-03-03 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prebuy_time', models.IntegerField(default=48, null=True, verbose_name='Время до выкупа заказа')),
            ],
        ),
    ]
