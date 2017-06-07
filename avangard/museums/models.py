from django.db import models
import datetime
from django.utils import timezone


# Create your models here.

class Museum(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    fullticket_price = models.IntegerField(default=0, verbose_name="Цена взрослый")
    full_coefficient = models.FloatField(default=0.0, verbose_name="Коэфф. стоимости взрослого")
    reduceticket_price = models.IntegerField(default=0, verbose_name="Цена льготный")
    reduce_coefficient = models.FloatField(default=0.0, verbose_name="Коэфф. стоимости льготного")
    audioguide_price = models.IntegerField(default=0, verbose_name="Цена аудиогоида")
    accompanying_guide_price = models.IntegerField(default=0, verbose_name="Цена сопровождающего гида")
    
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
    max_count_full = models.IntegerField(default=0, verbose_name="Квота билетов взрослых")
    max_count_reduce = models.IntegerField(default=0, verbose_name="Квота билетов льготных")

    def __str__(self):
    	return self.museum.name + " " + str(self.date) + " " + str(self.start_time) + " " + str(self.end_time)