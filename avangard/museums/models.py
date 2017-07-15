from django.db import models
import datetime
from django.utils import timezone


# Create your models here.

class Museum(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    fullticket_price = models.IntegerField(default=0, verbose_name="Цена взрослый")
    reduceticket_price = models.IntegerField(default=0, verbose_name="Цена льготный")
    audioguide_price = models.IntegerField(default=0, verbose_name="Цена аудиогоида")
    accompanying_guide_price = models.IntegerField(default=0, verbose_name="Цена сопровождающего гида")
    max_count = models.IntegerField(default=0, verbose_name="Макс. кол-во человек в группе")

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название компании")

    def __str__(self):
        return self.name


class Schedule(models.Model):
    museum = models.ForeignKey(Museum, on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    date = models.DateField(default=datetime.date.today, verbose_name="Дата")
    start_time = models.TimeField(default=timezone.now, verbose_name="Начало")
    end_time = models.TimeField(verbose_name="Конец", null=True)
    full_count = models.IntegerField(default=0, verbose_name="Квота билетов взрослых")
    reduce_count = models.IntegerField(default=0, verbose_name="Квота билетов льготных")
    full_coefficient_string = models.CharField(default="", null=True, max_length=1000, verbose_name="Коэфф. стоимости взрослого")
    reduce_coefficient_string = models.CharField(default="", null=True, max_length=1000, verbose_name="Коэфф. стоимости льготного")

    def _get_seance_full_price(self):
        full_coefficient = 1
        seance_coefficient_arr = self.full_coefficient_string.split(',')
        if len(seance_coefficient_arr) > 0:
            for seance_coefficient in seance_coefficient_arr:
                count_coeff = seance_coefficient.split('-')
                if count_coeff[0] != "":
                    tickets_value = int(count_coeff[0])
                    if self.full_count < tickets_value:
                        full_coefficient = float(count_coeff[1])
        return self.museum.fullticket_price * full_coefficient

    def _get_seance_reduce_price(self):
        reduce_coefficient = 1
        seance_coefficient_arr = self.reduce_coefficient_string.split(',')
        if len(seance_coefficient_arr) > 0:
            for seance_coefficient in seance_coefficient_arr:
                count_coeff = seance_coefficient.split('-')
                if count_coeff[0] != "":
                    tickets_value = int(count_coeff[0])
                    if self.reduce_count < tickets_value:
                        reduce_coefficient = float(count_coeff[1])
        return self.museum.reduceticket_price * reduce_coefficient

    full_price = property(_get_seance_full_price)
    reduce_price = property(_get_seance_reduce_price)


    def __str__(self):
        try:
            end_time = self.end_time.strftime("%H:%M")
            return str(self.date.strftime("%d.%m.%Y")) + ", " + self.start_time.strftime("%H:%M") + " - " + end_time + ", " + self.company.name
        except Exception:
            return self.start_time.strftime("%H:%M")
        # return self.museum.name + " " + str(self.date) + " " + str(self.start_time) + " " + str(self.end_time)
