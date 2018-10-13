from avangard.tourtickets.models import TtOrder
from rest_framework import serializers, viewsets


class TtOrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TtOrder
        fields = ('sender_name', 'sender_email', 'passenger', 'program', 'vessel', 'arrival_date',)
