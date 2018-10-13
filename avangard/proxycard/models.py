import json
from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField


# Create your models here.
class PcOrder(models.Model):
    NEW_STATUS = 1
    CONFIRMED_STATUS = 2
    STATUS_CHOICES = (
        (NEW_STATUS, 'New'),
        (CONFIRMED_STATUS, 'Confirmed')
    )
    sender_name = models.CharField(max_length=100, verbose_name="Создал заявку")
    sender_email = models.CharField(max_length=100, verbose_name="Электронная почта")
    added = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=100, verbose_name="ФИО")
    date = models.CharField(max_length=100, verbose_name="Дата рождения")
    passport = models.CharField(max_length=100, verbose_name="Паспортные данные")
    car_mark = models.CharField(max_length=100, verbose_name="Марка транспортного средства")
    car_plates = models.CharField(max_length=100, verbose_name="Государственные регистрационные знаки")

    vessel = models.CharField(max_length=100, verbose_name="Название корабля")
    arrival_date = models.CharField(max_length=100, verbose_name="Дата прибытия")
    tt_number = models.IntegerField(default=0, verbose_name="Номер туртикета")
    status = models.IntegerField(choices=STATUS_CHOICES, default=NEW_STATUS, verbose_name="Статус")

    def __str__(self):
        return str(self.id) + " " + self.sender_name + " " + str(self.added.strftime("%d-%m-%Y %H:%M"))

    class Meta:
        ordering = ('-pk',)
