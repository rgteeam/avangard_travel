from django.db import models
from avangard.museums.models import Museum, Schedule


class Order(models.Model):

    NEW_STATUS = 1
    CONFIRMED_STATUS = 2
    PURCHASED_STATUS = 3
    STATUS_CHOICES = (
        (NEW_STATUS, 'New'),
        (CONFIRMED_STATUS, 'Confirmed'),
        (PURCHASED_STATUS, 'Purchased'),
    )

    museum = models.ForeignKey(Museum, on_delete=models.CASCADE, null=True)
    seance = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=True)
    fullticket_count = models.IntegerField(default=0, verbose_name="Количество взрослых билетов")
    reduceticket_count = models.IntegerField(default=0, verbose_name="Количество льготных билетов")
    audioguide = models.BooleanField(default=False, verbose_name="Аудиогид")
    accompanying_guide = models.BooleanField(default=False, verbose_name="Сопровождающий гид")
    chat_id = models.IntegerField(null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=NEW_STATUS, verbose_name="Статус")
    name = models.CharField(max_length=100, verbose_name="ФИО")
    email = models.CharField(max_length=100, verbose_name="Электроная почта")
    phone = models.CharField(max_length=12, verbose_name="Номер телефона")

    def _get_full_price(self):
        full_price = self.fullticket_count * self.museum.fullticket_price + self.reduceticket_count * self.museum.reduceticket_price
        if (self.accompanying_guide):
            full_price += self.museum.accompanying_guide_price
        if (self.audioguide):
            full_price += self.museum.audioguide_price * (self.fullticket_count + self.reduceticket_count)
        return full_price

    full_price = property(_get_full_price)

    def __str__(self):
        return self.museum.name + " " + self.seance.start_time.strftime("%H:%M") + " " + str(self.full_price) + " руб."
