# Generated by Django 2.0.2 on 2018-10-10 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tourtickets', '0004_auto_20181010_2015'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ttorder',
            options={'ordering': ('pk',)},
        ),
    ]
