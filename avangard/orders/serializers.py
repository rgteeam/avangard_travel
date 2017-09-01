from avangard.orders.models import Order
from avangard.museums.serializers import MuseumSerializer, ScheduleSerializer
from avangard.museums.models import Museum, Schedule
from rest_framework import serializers


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES, required=False)
    museum = MuseumSerializer(read_only=True)
    seance = ScheduleSerializer(read_only=True)
    fullticket_store = serializers.CharField(read_only=True)
    reduceticket_store = serializers.CharField(read_only=True)
    museum_id = serializers.PrimaryKeyRelatedField(queryset=Museum.objects.all(), source='museum', write_only=True)
    seance_id = serializers.PrimaryKeyRelatedField(queryset=Schedule.objects.all(), source='seance', write_only=True)
    fullticket_count = serializers.IntegerField(min_value=0)
    reduceticket_count = serializers.IntegerField(min_value=0)

    class Meta:
        model = Order
        fields = (
            'pk', 'museum', 'seance', 'museum_id', 'seance_id', 'fullticket_count', 'fullticket_store', 'reduceticket_store','reduceticket_count', 'audioguide',
            'accompanying_guide', 'full_price', 'added', 'updated', 'chat_id', 'user_id', 'status', 'name', 'email',
            'phone')


    def validate(self, data):
        seance = data["seance"]
        fullticket_count = int(data["fullticket_count"])
        reduceticket_count = int(data["reduceticket_count"])
        if seance.full_count < fullticket_count:
            raise serializers.ValidationError({'fullticket_count': 'Too much full tickets'})
        if seance.reduce_count < reduceticket_count:
            raise serializers.ValidationError({'reduceticket_count': 'Too much reduce tickets'})
        if seance.museum.max_count < reduceticket_count + fullticket_count:
            raise serializers.ValidationError('Max group count error')
        return data
