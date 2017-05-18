from rest_framework import viewsets, filters, generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from avangard.museums.serializers import MuseumSerializer, ScheduleSerializer
import django_filters.rest_framework
from django.db import models as django_models
from avangard.museums.models import Museum, Schedule
from datetime import date, datetime, time, timedelta


class ScheduleFilter(filters.FilterSet):
    def get_closest(self, queryset, name, value):
        range_start = (datetime.combine(date.today(), value) - timedelta(minutes=30)).time()
        range_end = (datetime.combine(date.today(), value) + timedelta(minutes=30)).time()
        print(range_end)
        closest_qs = queryset.filter(start_time__range=(range_start, range_end)).order_by('start_time')

        return closest_qs

    start_time = django_filters.TimeFilter(name="start_time", method='get_closest')

    class Meta:
        model = Schedule
        fields = ['museum_id', 'date', 'start_time']

    filter_overrides = {
        django_models.DateTimeField: {
            'filter_class': django_filters.IsoDateTimeFilter
        },
    }


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'museums': reverse('museum-list', request=request),
    })


class MuseumViewSet(viewsets.ModelViewSet):
    queryset = Museum.objects.all()
    serializer_class = MuseumSerializer


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    filter_class = ScheduleFilter