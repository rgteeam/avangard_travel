# Generated by Django 2.0.2 on 2018-12-18 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0030_auto_20181218_2314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='user_id',
        ),
        migrations.AddField(
            model_name='superorder',
            name='chat_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='superorder',
            name='user_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]