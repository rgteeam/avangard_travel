from avangard.chat.models import ChatRoom, Message
from django.contrib.auth.models import User
from rest_framework import serializers
from avangard.account.serializers import ShortUserSerializer

# Сообщение в чате

class MessageSerializer(serializers.HyperlinkedModelSerializer):
    sender = ShortUserSerializer(read_only=True)
    recipient = ShortUserSerializer(read_only=True)
    sender_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='sender', write_only=True)
    recipient_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='recipient', write_only=True)
    room_id = serializers.PrimaryKeyRelatedField(queryset=ChatRoom.objects.all(), source='room', write_only=True)
    timestamp = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", read_only=True)

    class Meta:
        model = Message
        fields = (
        'pk', 'text', 'sender', 'recipient', 'sender_id', 'recipient_id', 'status', 'room_id', 'timestamp')

# Комната в чате (содержит информацию о комнате, количество непрочитанных сообщений и последнее сообщение)

class ChatRoomSerializer(serializers.HyperlinkedModelSerializer):
    last_message = MessageSerializer(read_only=True)
    unread_count = serializers.IntegerField(read_only=True)
    room_admin = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = ChatRoom
        fields = ('pk', 'name', 'type', 'last_message', 'unread_count', 'room_admin')
