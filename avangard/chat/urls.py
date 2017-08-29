from django.conf.urls import url, include

from . import views



urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(\d+)', views.chat_room, name='chat_room'),
    url(r'^get_dialogs/(\d+)', views.get_dialogs, name='get_dialogs'),
    ]