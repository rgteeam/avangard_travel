from avangard.orders.models import Order, SuperOrder
from avangard.museums.serializers import MuseumSerializer, ScheduleSerializer
from avangard.museums.models import Museum, Schedule
from rest_framework import serializers
import json
from django.forms.models import model_to_dict


class StoreField(serializers.Field):

    def to_representation(self, obj):
        array = []
        data = obj.strip('[').rstrip(']')
        objects = data.split(', ')
        for cur_object in objects:
            object_data = cur_object.strip('{').rstrip('}')
            key = int(object_data.split(':')[0].strip('"').rstrip('"'))
            value = float(object_data.split(':')[1])
            array.append({
                'count': key,
                'price': value,
            })
        return array


class StoreField2(serializers.Field):

    def to_representation(self, obj):
        array = []
        for i in obj:
            order = Order.objects.get(pk=i)
            array.append(model_to_dict(order))
        return array


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES, required=False)
    museum = MuseumSerializer(read_only=True)
    seance = ScheduleSerializer(read_only=True)
    fullticket_store = StoreField(read_only=True)
    reduceticket_store = StoreField(read_only=True)
    museum_id = serializers.PrimaryKeyRelatedField(queryset=Museum.objects.all(), source='museum', write_only=True)
    seance_id = serializers.PrimaryKeyRelatedField(queryset=Schedule.objects.all(), source='seance', write_only=True)
    fullticket_count = serializers.IntegerField(min_value=0)
    reduceticket_count = serializers.IntegerField(min_value=0)

    class Meta:
        model = Order
        fields = (
            'pk', 'museum', 'seance', 'museum_id', 'seance_id', 'fullticket_count', 'fullticket_store', 'reduceticket_store', 'reduceticket_count', 'audioguide',
            'accompanying_guide', 'full_price', 'added', 'updated', 'status', 'name', 'email', 'phone', 'superorder')

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


class SuperOrderSerializer(serializers.ModelSerializer):
    orders = StoreField2(read_only=True)
    status = serializers.ChoiceField(choices=SuperOrder.STATUS_CHOICES, required=False)
    museum = MuseumSerializer(read_only=True)
    seance = ScheduleSerializer(read_only=True)
    museum_id = serializers.PrimaryKeyRelatedField(queryset=Museum.objects.all(), source='museum', write_only=True)
    seance_id = serializers.PrimaryKeyRelatedField(queryset=Schedule.objects.all(), source='seance', write_only=True)
    fullticket_count = serializers.IntegerField(min_value=0)
    reduceticket_count = serializers.IntegerField(min_value=0)

    class Meta:
        model = SuperOrder
        fields = (
            'pk', 'museum', 'seance', 'museum_id', 'seance_id', 'fullticket_count', 'reduceticket_count', 'audioguide',
            'accompanying_guide', 'added', 'updated', 'user_id', 'status', 'name', 'email',
            'phone', 'qr_code', 'orders', 'start_time', 'end_time', 'date', 'totalPrice')

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
