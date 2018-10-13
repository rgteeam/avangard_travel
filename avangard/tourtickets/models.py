import json
from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField


# Create your models here.
class TtOrder(models.Model):
    NEW_STATUS = 1
    CONFIRMED_STATUS = 2
    STATUS_CHOICES = (
        (NEW_STATUS, 'New'),
        (CONFIRMED_STATUS, 'Confirmed')
    )
    sender_name = models.CharField(max_length=100, verbose_name="Создал заявку")
    sender_email = models.CharField(max_length=100, verbose_name="Электронная почта")
    added = models.DateTimeField(auto_now_add=True)
    passenger = JSONField(default=list([]))
    program = models.CharField(max_length=500, verbose_name="Программа пребывания")
    vessel = models.CharField(max_length=100, verbose_name="Название корабля")
    arrival_date = models.CharField(max_length=100, verbose_name="Дата прибытия")
    service_dates = models.CharField(max_length=100, verbose_name="Даты обслуживания")
    passenger_count = models.IntegerField(default=0, verbose_name="Кол-во пассажиров")
    tt_number = models.IntegerField(default=0, verbose_name="Номер туртикета")
    status = models.IntegerField(choices=STATUS_CHOICES, default=NEW_STATUS, verbose_name="Статус")

    def __str__(self):
        return str(self.id) + " " + self.sender_name + " " + str(self.added.strftime("%d-%m-%Y %H:%M")) + " " + str(self.passenger_count)

    def save(self, **kwargs):
        self.service_dates = self.arrival_date
        self.passenger_count = len(self.passenger)
        super(TtOrder, self).save()

    class Meta:
        ordering = ('-pk',)
