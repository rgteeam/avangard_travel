from django.db import models
import datetime
from django.utils import timezone


# Create your models here.

class Museum(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    max_count = models.IntegerField(default=0, verbose_name="Квота билетов")
    audioguide = models.BooleanField(default=False, verbose_name="Аудиогид")
    accompanying_guide = models.BooleanField(default=False, verbose_name="Сопровождающий гид")


class Schedule(models.Model):
    museum = models.ForeignKey(Museum, on_delete=models.CASCADE, null=True)
    date = models.DateField(default=datetime.date.today, verbose_name="Дата")
    start_time = models.TimeField(default=timezone.now, verbose_name="Начало")
    end_time = models.TimeField(verbose_name="Конец", null=True)
    max_count = models.IntegerField(default=0, verbose_name="Квота билетов")
