from avangard.orders.models import Order
from avangard.museums.models import Museum, Schedule
from rest_framework import serializers, viewsets


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES, required=False)
    class Meta:
        model = Order
        fields = (
        'pk', 'museum', 'seance', 'fullticket_count', 'reduceticket_count', 'audioguide', 'accompanying_guide',
        'full_price', 'chat_id', 'status', 'name', 'email', 'phone')
