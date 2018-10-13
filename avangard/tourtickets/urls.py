from django.conf.urls import url, include
from rest_framework import routers

from . import views

urlpatterns = [
    url(r'^$', views.tourtickets_index, name='tourtickets_index'),
    url(r'^edit/(\d+)', views.tourtickets_edit, name='tourtickets_edit'),
    url(r'^download/(\d+)', views.tourtickets_create, name='tourtickets_create'),
    url(r'^create/(\d+)', views.tourtickets_create, name='tourtickets_create'),
    url(r'^delete/(\d+)', views.tourtickets_delete, name='tourtickets_delete'),

]
