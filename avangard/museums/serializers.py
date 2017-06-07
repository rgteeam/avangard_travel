from avangard.museums.models import Museum, Schedule
from rest_framework import serializers, viewsets


class MuseumSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Museum
        fields = ('pk', 'name', 'fullticket_price', 'full_coefficient', 'reduceticket_price', 'reduce_coefficient', 'audioguide_price', 'accompanying_guide_price')


class ScheduleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Schedule
        fields = ('pk', 'museum_id', 'max_count_full', 'max_count_reduce', 'start_time', 'end_time', 'date')
