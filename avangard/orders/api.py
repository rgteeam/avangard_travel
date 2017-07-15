from rest_framework import viewsets, filters, generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from avangard.orders.serializers import OrderSerializer
import django_filters.rest_framework
from django.db import models as django_models
from avangard.orders.models import Order
from django.db.models import Q
import datetime


class OrderFilter(filters.FilterSet):

    def filter_date_gte(self, queryset, name, value):
        date = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        qs = queryset.filter(Q(seance__date__gt=date.date()) | (Q(seance__date=date.date()) & Q(seance__start_time__gt=date.time())))
        return qs

    def filter_date_lte(self, queryset, name, value):
        date = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        qs = queryset.filter(Q(seance__date__lte=date.date()) | (Q(seance__date=date.date()) & Q(seance__start_time__lte=date.time())))
        return qs

    date_lte = django_filters.Filter(name="date_lte", method="filter_date_lte")
    date_gte = django_filters.Filter(name="date_gte", method="filter_date_gte")
    class Meta:
        model = Order
        fields = {'chat_id', 'user_id', 'date_gte', 'date_lte'}


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_class = OrderFilter
    ordering_fields = ('pk')
