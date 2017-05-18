"""avangard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from rest_framework import routers
from avangard.museums.api import MuseumViewSet,ScheduleViewSet

from . import views

router = routers.DefaultRouter()
router.register(r'museums', MuseumViewSet, 'Museum')
router.register(r'schedule', ScheduleViewSet, 'Schedule')

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^museums/(\d+)/schedule/', views.museum_schedule, name='museum_schedule'),
    url(r'^schedule/delete/(\d+)', views.schedule_delete, name='schedule_delete'),
    url(r'^schedule/update/(\d+)', views.schedule_update, name='schedule_update'),
    url(r'^schedule/create', views.schedule_create, name='schedule_create'),
    url(r'^museums/create/', views.create_museum_view, name='create_museum'),
]

