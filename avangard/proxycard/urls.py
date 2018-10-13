from django.conf.urls import url, include
from rest_framework import routers

from . import views

urlpatterns = [
    url(r'^$', views.proxycard_index, name='proxycard_index'),
    url(r'^edit/(\d+)', views.proxycard_edit, name='proxycard_edit'),
    url(r'^download/(\d+)', views.proxycard_create, name='proxycard_create'),
    url(r'^create/(\d+)', views.proxycard_create, name='proxycard_create'),
    url(r'^delete/(\d+)', views.proxycard_delete, name='proxycard_delete'),

]
