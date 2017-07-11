from channels.channel import Group


def ws_connect(message):
    message.reply_channel.send({"accept": True})
    Group('orders_table').add(message.reply_channel)


def ws_message(message):
    Group('orders_table').send({'text': message.content['text']})


def ws_disconnect(message):
    Group('orders_table').discard(message.reply_channel)
