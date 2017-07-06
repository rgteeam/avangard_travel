from avangard.orders.models import Order
from avangard.museums.serializers import MuseumSerializer, ScheduleSerializer
from avangard.museums.models import Museum, Schedule
from rest_framework import serializers


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES, required=False)
    museum = MuseumSerializer(read_only=True)
    seance = ScheduleSerializer(read_only=True)
    museum_id = serializers.PrimaryKeyRelatedField(queryset=Museum.objects.all(), source='museum', write_only=True)
    seance_id = serializers.PrimaryKeyRelatedField(queryset=Schedule.objects.all(), source='seance', write_only=True)
    class Meta:
        model = Order
        fields = (
        'pk','museum','seance', 'museum_id','seance_id','fullticket_count', 'reduceticket_count', 'audioguide', 'accompanying_guide',
        'full_price', 'chat_id', 'user_id', 'status', 'name', 'email', 'phone')
