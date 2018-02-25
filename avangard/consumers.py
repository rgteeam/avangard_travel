from channels.channel import Group
from avangard.chat.models import Message
import json


def ws_connect_orders(message):
    message.reply_channel.send({"accept": True})
    Group('orders_table').add(message.reply_channel)


def ws_message_orders(message):
    Group('orders_table').send({'text': message.content['text']})


def ws_disconnect_orders(message):
    Group('orders_table').discard(message.reply_channel)


def ws_connect_schedule(message):
    message.reply_channel.send({"accept": True})
    Group('schedule_table').add(message.reply_channel)


def ws_message_schedule(message):
    Group('schedule_table').send({'text': message.content['text']})


def ws_disconnect_schedule(message):
    Group('schedule_table').discard(message.reply_channel)


def ws_connect_chat(message, room_id):
    message.reply_channel.send({"accept": True})
    print("admin connected")
    Group('admin-chat-%s' % room_id).add(message.reply_channel)


def ws_message_chat(message, room_id):
    Group('admin-chat-%s' % room_id).send({'text': message.content['text']})


def ws_disconnect_chat(message, room_id):
    Group('admin-chat-%s' % room_id).discard(message.reply_channel)


def ws_user_connect_chat(message, user_id):

    unread_count = len(Message.objects.filter(status=1, recipient__pk=user_id))

    text = {"event": "user_connected", "unread_count": unread_count}
    message.reply_channel.send({"accept": True, "text": json.dumps(text)})
    print("user connected")
    Group('user-chat-%s' % user_id).add(message.reply_channel)


def ws_user_message_chat(message, user_id):
    Group('user-chat-%s' % user_id).send({'text': message.content['text']})


def ws_user_disconnect_chat(message, user_id):
    Group('user-chat-%s' % user_id).discard(message.reply_channel)
