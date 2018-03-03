from django.db import models
from avangard.museums.models import Museum, Schedule
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.channel import Group
from django.contrib.postgres.fields import JSONField, ArrayField
from avangard import settings
import json
import qrcode


class Order(models.Model):
    NEW_STATUS = 1
    CONFIRMED_STATUS = 2
    PURCHASED_STATUS = 3
    DENY_STATUS = 4
    SCANNED_STATUS = 5
    STATUS_CHOICES = (
        (NEW_STATUS, 'New'),
        (CONFIRMED_STATUS, 'Confirmed'),
        (PURCHASED_STATUS, 'Purchased'),
        (DENY_STATUS, 'Deny'),
        (SCANNED_STATUS, 'Scanned')
    )

    museum = models.ForeignKey(Museum, on_delete=models.CASCADE, null=True)
    seance = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=True)
    fullticket_count = models.IntegerField(default=0, verbose_name="Количество взрослых билетов")
    reduceticket_count = models.IntegerField(default=0, verbose_name="Количество льготных билетов")
    fullticket_store = JSONField(default=list([]))
    reduceticket_store = JSONField(default=list([]))
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
    qr_code = models.FileField(upload_to='qr_code', blank=True)

    def save(self, **kwargs):
        if self.status == "2":
            self.qr_code = self.generate_qrcode()
        super(Order, self).save()

    def generate_qrcode(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        data = '%s' % self.fullticket_count
        qr.add_data(data)
        qr.make(fit=True)
        filename = '%s.png' % self.pk
        img = qr.make_image()
        img.save(settings.MEDIA_ROOT + "/qr_code/" + filename)
        return "/qr_code/" + filename

    def _get_full_price(self):

        full_price = get_price(self.fullticket_store) + get_price(self.reduceticket_store)

        if self.accompanying_guide:
            full_price += self.museum.accompanying_guide_price
        if self.audioguide:
            full_price += self.museum.audioguide_price * (self.fullticket_count + self.reduceticket_count)
        return full_price

    full_price = property(_get_full_price)

    def __str__(self):
        return self.name + ", " + str(
            self.seance.date.strftime("%d.%m.%Y")) + ", " + self.museum.name + ", " + self.seance.start_time.strftime(
            "%H:%M") + "-" + self.seance.end_time.strftime("%H:%M") + " " + str(self.full_price) + " руб."

    class Meta:
        ordering = ('-pk',)


def get_price(store):
    ticket_data = json.loads(store)
    price = 0
    for element in ticket_data:
        for key, val in element.items():
            price += int(key) * int(val)
    return price


def new_order(instance):
    fullticket_data_list = list()
    fullticket_data_dict = dict()
    fullticket_data_dict[instance.fullticket_count] = instance.seance.full_price
    fullticket_data_list.append(fullticket_data_dict)
    instance.fullticket_store = json.dumps(fullticket_data_list)
    reduceticket_data_list = list()
    reduceticket_data_dict = dict()
    reduceticket_data_dict[instance.reduceticket_count] = instance.seance.reduce_price
    reduceticket_data_list.append(reduceticket_data_dict)
    instance.reduceticket_store = json.dumps(reduceticket_data_list)
    instance.save()
    instance.seance.full_count -= instance.fullticket_count
    instance.seance.reduce_count -= instance.reduceticket_count
    instance.seance.save()


def tickets_added(ticket_exist, ticket_store, ticket_count, price, ticket_kind, instance):
    ticket_data = json.loads(ticket_store)
    if ticket_exist == 0:
        ticket_data = [{ticket_count - ticket_exist: price}]
    else:
        ticket_data.append({ticket_count - ticket_exist: price})
    if ticket_kind == "fullticket_store":
        instance.fullticket_store = json.dumps(ticket_data)
        instance.save()
        instance.seance.full_count -= ticket_count - ticket_exist
        instance.seance.save()
    elif ticket_kind == "reduceticket_store":
        instance.reduceticket_store = json.dumps(ticket_data)
        instance.save()
        instance.seance.reduce_count -= ticket_count - ticket_exist
        instance.seance.save()


def tickets_removed(ticket_exist, ticket_store, ticket_count, instance, ticket_kind):
    ticket_data = json.loads(ticket_store)
    need_delete = ticket_exist - ticket_count
    lens = len(ticket_data) - 1
    if ticket_kind == "fullticket_store":
        instance.seance.full_count += need_delete
        instance.seance.save()
    elif ticket_kind == "reduceticket_store":
        instance.seance.reduce_count += need_delete
        instance.seance.save()
    for i, dic in enumerate(reversed(ticket_data)):
        for key, val in dic.items():
            if need_delete > 0:
                if int(key) >= need_delete:
                    del ticket_data[lens - i]
                    if (len(ticket_data) > 0 and int(key) != need_delete) or (len(ticket_data) == 0):
                        ticket_data.append({int(key) - need_delete: val})
                    need_delete = need_delete - int(key)
                    if ticket_kind == "fullticket_store":
                        instance.fullticket_store = json.dumps(ticket_data)
                    elif ticket_kind == "reduceticket_store":
                        instance.reduceticket_store = json.dumps(ticket_data)
                    instance.save()
                    break
                if int(key) < need_delete:
                    del ticket_data[lens - i]
                    need_delete = need_delete - int(key)
                    if ticket_kind == "fullticket_store":
                        instance.fullticket_store = json.dumps(ticket_data)
                    elif ticket_kind == "reduceticket_store":
                        instance.reduceticket_store = json.dumps(ticket_data)
                    instance.save()
                    break
            else:
                return


@receiver(post_save, sender=Order, dispatch_uid="update_tickets_counts")
def update_tickets_counts(sender, instance, update_fields, created, **kwargs):
    if update_fields == {'fullticket_store'} or update_fields == {'reduceticket_store'}:
        return
    if created:  # заказ создается впервые
        new_order(instance)
    else:  # заказ редактируется
        fullticket_exist = sum([int(val) for dic in json.loads(instance.fullticket_store) for val in dic.keys()])
        reduceticket_exist = sum([int(val) for dic in json.loads(instance.reduceticket_store) for val in dic.keys()])

        if instance.fullticket_count > fullticket_exist:  # добавлены новые взрослые билеты
            tickets_added(fullticket_exist, instance.fullticket_store, instance.fullticket_count,
                          instance.seance.full_price, 'fullticket_store', instance)

        if instance.reduceticket_count > reduceticket_exist:  # добавлены новые льготные билеты
            tickets_added(reduceticket_exist, instance.reduceticket_store, instance.reduceticket_count,
                          instance.seance.reduce_price, 'reduceticket_store', instance)

        if instance.fullticket_count < fullticket_exist:  # взрослых билетов стало меньше
            tickets_removed(fullticket_exist, instance.fullticket_store, instance.fullticket_count, instance,
                            'fullticket_store')

        if instance.reduceticket_count < reduceticket_exist:  # льготных билетов стало меньше
            tickets_removed(reduceticket_exist, instance.reduceticket_store, instance.reduceticket_count, instance,
                            'reduceticket_store')


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
                                     "company": instance.seance.company.pk}})
    })


@receiver(post_delete, sender=Order)
def order_deleted(sender, instance, **kwargs):
    instance.seance.full_count += instance.fullticket_count
    instance.seance.reduce_count += instance.reduceticket_count
    instance.seance.save()

    Group('orders_table').send({
        "text": json.dumps({"event": "order_deleted", "item": {"pk": instance.pk}})
    })
