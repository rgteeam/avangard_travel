# Generated by Django 2.0.2 on 2018-12-18 20:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0029_auto_20181024_1522'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='chat_id',
        ),
        migrations.RemoveField(
            model_name='order',
            name='qr_code',
        ),
        migrations.RemoveField(
            model_name='order',
            name='voucher',
        ),
    ]
