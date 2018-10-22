from avangard.museums.models import Museum, Schedule, Company
from rest_framework import serializers, viewsets


class MuseumSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Museum
        fields = ('pk', 'name', 'fullticket_price', 'reduceticket_price', 'audioguide_price', 'accompanying_guide_price', 'max_count', 'voucher_numbers')


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ('pk', 'name', 'contract_number')


class ScheduleSerializer(serializers.HyperlinkedModelSerializer):

    start_time = serializers.TimeField(format="%H:%M")
    end_time = serializers.TimeField(format="%H:%M")

    class Meta:
        model = Schedule
        fields = ('pk', 'museum_id', 'full_count', 'reduce_count', 'full_price', 'reduce_price', 'full_coefficient_string', 'reduce_coefficient_string', 'start_time', 'end_time', 'date', 'company_id')
