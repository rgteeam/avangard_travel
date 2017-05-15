from django.db import models

# Create your models here.

class Museum(models.Model):
    name = models.CharField(max_length=50, verbose_name = "Название")
    max_count = models.IntegerField(default=0, verbose_name = "Квота билетов")
    audioguide = models.BooleanField(default=False, verbose_name = "Аудиогид")
    accompanying_guide = models.BooleanField(default=False, verbose_name = "Сопровождающий гид")