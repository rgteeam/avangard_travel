from channels.routing import route


channel_routing = [
    route("websocket.connect", "avangard.consumers.ws_connect_orders", path=r"^ws/orders/"),
    route("websocket.receive", "avangard.consumers.ws_message_orders", path=r"^ws/orders/"),
    route("websocket.disconnect", "avangard.consumers.ws_disconnect_orders", path=r"^ws/orders/"),

    route("websocket.connect", "avangard.consumers.ws_connect_schedule", path=r"^ws/schedule/"),
    route("websocket.receive", "avangard.consumers.ws_message_schedule", path=r"^ws/schedule/"),
    route("websocket.disconnect", "avangard.consumers.ws_disconnect_schedule", path=r"^ws/schedule/"),

    route("websocket.connect", "avangard.consumers.ws_connect_chat", path=r"^ws/chat/(?P<room_id>[0-9]+)"),
    route("websocket.receive", "avangard.consumers.ws_message_chat", path=r"^ws/chat/(?P<room_id>[0-9]+)"),
    route("websocket.disconnect", "avangard.consumers.ws_disconnect_chat", path=r"^ws/chat/(?P<room_id>[0-9]+)"),

    route("websocket.connect", "avangard.consumers.ws_user_connect_chat", path=r"^ws/chat-user/(?P<user_id>[0-9]+)"),
    route("websocket.receive", "avangard.consumers.ws_user_message_chat", path=r"^ws/chat-user/(?P<user_id>[0-9]+)"),
    route("websocket.disconnect", "avangard.consumers.ws_user_disconnect_chat", path=r"^ws/chat-user/(?P<user_id>[0-9]+)"),
]
