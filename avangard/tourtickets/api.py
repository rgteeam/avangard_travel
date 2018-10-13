from rest_framework import viewsets, generics
from avangard.tourtickets.serializers import TtOrderSerializer
from avangard.tourtickets.models import TtOrder


class TourticketViewSet(viewsets.ModelViewSet):
    queryset = TtOrder.objects.all()
    serializer_class = TtOrderSerializer
