from django.db import models
from avangard.museums.models import Museum, Schedule
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.channel import Group
import json


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
    chat_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=NEW_STATUS, verbose_name="Статус")
    name = models.CharField(max_length=100, verbose_name="ФИО")
    email = models.CharField(max_length=100, verbose_name="Электроная почта")
    phone = models.CharField(max_length=12, verbose_name="Номер телефона")
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def _get_full_price(self):
        full_price = self.fullticket_count * self.museum.fullticket_price + self.reduceticket_count * self.museum.reduceticket_price
        if self.accompanying_guide:
            full_price += self.museum.accompanying_guide_price
        if self.audioguide:
            full_price += self.museum.audioguide_price * (self.fullticket_count + self.reduceticket_count)
        return full_price

    full_price = property(_get_full_price)

    def __str__(self):
        return self.name + ", " + str(self.seance.date.strftime("%d.%m.%Y")) + ", " + self.museum.name + ", " + self.seance.start_time.strftime("%H:%M") + "-" + self.seance.end_time.strftime("%H:%M") + " " + str(self.full_price) + " руб."

    class Meta:
        ordering = ('-pk',)


@receiver(post_save, sender=Order, dispatch_uid="update_tickets_counts")
def update_tickets_counts(sender, instance, created, **kwargs):
    if created:
        instance.seance.full_count -= instance.fullticket_count
        instance.seance.reduce_count -= instance.reduceticket_count
        instance.seance.save()

@receiver(post_save, sender=Order, dispatch_uid="order_created")
def order_created(sender, instance, created, **kwargs):

    event_name = "order_created" if created else "order_updated"

    Group('orders_table').send({
        "text": json.dumps({"event": event_name,
                            "item": {"pk": instance.pk,
                                     "museum": instance.museum.name,
                                     "seance": instance.seance.time_str,
                                     "date": instance.seance.date.strftime("%Y-%m-%d"),
                                     "full_price": instance.full_price,
                                     "fullticket_count": instance.fullticket_count,
                                     "reduceticket_count": instance.reduceticket_count,
                                     "audioguide": instance.audioguide,
                                     "accompanying_guide": instance.accompanying_guide,
                                     "status": int(instance.status),
                                     "name": instance.name,
                                     "email": instance.email,
                                     "phone": instance.phone,
                                     "company": instance.seance.company.pk}
        })
    })

@receiver(post_delete, sender=Order)
def order_deleted(sender, instance, **kwargs):

    instance.seance.full_count += instance.fullticket_count
    instance.seance.reduce_count += instance.reduceticket_count
    instance.seance.save()

    Group('orders_table').send({
        "text": json.dumps({"event": "order_deleted", "item": {"pk": instance.pk}})
    })