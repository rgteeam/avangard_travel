from rest_framework import viewsets, generics
from avangard.proxycard.serializers import PcOrderSerializer
from avangard.proxycard.models import PcOrder


class ProxycardViewSet(viewsets.ModelViewSet):
    queryset = PcOrder.objects.all()
    serializer_class = PcOrderSerializer
