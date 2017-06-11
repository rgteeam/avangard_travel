from rest_framework import viewsets, filters, generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from avangard.orders.serializers import OrderSerializer
import django_filters.rest_framework
from django.db import models as django_models
from avangard.orders.models import Order


class OrderFilter(filters.FilterSet):
    class Meta:
        model = Order
        fields = {'chat_id'}


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_class = OrderFilter
    ordering_fields = ('pk')
