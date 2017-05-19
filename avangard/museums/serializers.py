from avangard.museums.models import Museum, Schedule
from rest_framework import serializers, viewsets


class MuseumSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Museum
        fields = ('pk', 'name', 'max_count', 'audioguide', 'accompanying_guide')


class ScheduleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Schedule
        fields = ('pk', 'museum_id', 'max_count', 'start_time', 'end_time', 'date')
