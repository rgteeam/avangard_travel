from channels.channel import Group


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
