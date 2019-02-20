# Generated by Django 2.0.2 on 2018-10-24 09:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0026_order_voucher'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuperOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullticket_count', models.IntegerField(default=0, verbose_name='Количество взрослых билетов')),
                ('reduceticket_count', models.IntegerField(default=0, verbose_name='Количество льготных билетов')),
                ('audioguide', models.BooleanField(default=False, verbose_name='Аудиогид')),
                ('accompanying_guide', models.BooleanField(default=False, verbose_name='Сопровождающий гид')),
                ('status', models.IntegerField(choices=[(1, 'New'), (2, 'Confirmed'), (3, 'Purchased'), (4, 'Ready'), (5, 'Passed'), (6, 'Scanned'), (7, 'Deny')], default=1, verbose_name='Статус')),
                ('name', models.CharField(max_length=100, verbose_name='ФИО')),
                ('email', models.CharField(max_length=100, verbose_name='Электроная почта')),
                ('phone', models.CharField(max_length=12, verbose_name='Номер телефона')),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('qr_code', models.CharField(blank=True, max_length=100, verbose_name='QR code')),
                ('voucher', models.CharField(blank=True, max_length=100, verbose_name='Ваучер')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='superorder',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.SuperOrder'),
        ),
    ]