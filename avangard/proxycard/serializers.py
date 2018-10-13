from avangard.proxycard.models import PcOrder
from rest_framework import serializers, viewsets


class PcOrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PcOrder
        fields = ('sender_name', 'sender_email', 'name', 'date', 'passport', 'car_mark', 'car_plates', 'vessel', 'arrival_date',)
