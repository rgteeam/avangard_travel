from django.db import models


# Create your models here.
class OrderSettings(models.Model):
    prebuy_time = models.IntegerField(null=True, blank=False, verbose_name="Время до выкупа заказа", default=48)

    def __str__(self):
        return str(self.prebuy_time)
