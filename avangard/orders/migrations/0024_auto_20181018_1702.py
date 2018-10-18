# Generated by Django 2.0.2 on 2018-10-18 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0023_auto_20180314_0215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(1, 'New'), (2, 'Confirmed'), (3, 'Purchased'), (4, 'Ready'), (5, 'Pass'), (6, 'Scanned'), (7, 'Deny')], default=1, verbose_name='Статус'),
        ),
    ]