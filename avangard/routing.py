from channels.routing import route


channel_routing = [
    route("websocket.connect", "avangard.consumers.ws_connect"),
    route("websocket.receive", "avangard.consumers.ws_message"),
    route("websocket.disconnect", "avangard.consumers.ws_disconnect"),
]
