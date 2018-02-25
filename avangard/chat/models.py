from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.channel import Group
from django.core.serializers.json import DjangoJSONEncoder
import json


# Create your models here.

class ChatRoom(models.Model):
    MUSEUM_ROOM = 1
    STUFF_ROOM = 2
    TECHNICAL_ROOM = 3
    TYPE_CHOICES = (
        (MUSEUM_ROOM, 'Museum'),
        (STUFF_ROOM, 'Other stuff'),
        (TECHNICAL_ROOM, 'Technical'),
    )

    type = models.IntegerField(choices=TYPE_CHOICES, default=MUSEUM_ROOM, verbose_name="Тип чата")
    name = models.CharField(max_length=100, verbose_name="Название чата")
    room_admin = models.ForeignKey(User, related_name="Admin", default=User.objects.filter(is_superuser=True)[0].pk, on_delete=models.PROTECT)
    # room_admin = models.ForeignKey(User, related_name="Admin")

    def __str__(self):
        return self.name


class Message(models.Model):
    NEW = 1
    READ = 2
    MESSAGE_STATUS = (
        (NEW, 'New'),
        (READ, 'Read'),
    )

    status = models.IntegerField(choices=MESSAGE_STATUS, default=NEW, verbose_name="Стутус сообщения")

    room = models.ForeignKey(ChatRoom, on_delete=models.PROTECT)
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE, null=True)
    recipient = models.ForeignKey(User, related_name="recipient", on_delete=models.CASCADE, null=True)
    text = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self):
        return str(self.sender) + " – " + str(self.recipient) + ": " + self.text


@receiver(post_save, sender=Message, dispatch_uid="new_message")
def new_message(sender, instance, created, **kwargs):
    if created:
        event_name = "new_message"
        message = {
            "text": json.dumps({"event": event_name,
                                "item": {"pk": instance.pk,
                                         "text": instance.text,
                                         "sender": {
                                             "pk": instance.sender.pk,
                                             "first_name": instance.sender.first_name,
                                             "last_name": instance.sender.last_name,
                                         },
                                         "recipient": {
                                             "pk": instance.recipient.pk,
                                             "first_name": instance.recipient.first_name,
                                             "last_name": instance.recipient.last_name,
                                         },
                                         "status": instance.status,
                                         "timestamp": instance.timestamp,
                                         "room_id": instance.room.pk}
                                }, cls=DjangoJSONEncoder)
        }
        Group('admin-chat-%s' % instance.room.pk).send(message)
        if instance.sender.is_staff:
            Group('user-chat-%s' % instance.recipient.pk).send(message)
        else:
            Group('user-chat-%s' % instance.sender.pk).send(message)
