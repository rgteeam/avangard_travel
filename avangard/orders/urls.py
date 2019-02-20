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

from . import views

urlpatterns = [
    url(r'^$', views.orders_index, name='orders_index'),
    url(r'^old/', views.get_old_orders, name='get_old_orders'),
    url(r'^get_seances/', views.get_seances_for_date, name='get_seances'),
    url(r'^get_aggregated_seances/', views.get_aggregated_seances, name='get_aggregated_seances'),
    url(r'^create_sorder/', views.create_sorder, name='create_sorder'),
    url(r'^created_sorder/', views.created_sorder, name='created_sorder'),
    url(r'^get_timeblock_data/', views.get_timeblock_data, name='get_timeblock_data'),
    url(r'^ticket_receipt/', views.ticket_receipt, name='ticket_receipt'),
    url(r'^edit/(\d+)', views.edit_order, name='edit_order'),
    url(r'^info/(\d+)', views.info_sorder, name='info_sorder'),
    url(r'^info/', views.info_sorder, name='info_sorder'),
    url(r'^delete/(\d+)', views.delete_order, name='delete_order'),
    url(r'^sodelete/(\d+)', views.delete_sorder, name='delete_sorder'),
    url(r'^update_status/(\d+)', views.update_order_status, name='update_status'),
    url(r'^seance_selected/', views.seance_selected, name='seance_selected'),
]
