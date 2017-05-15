from avangard.museums.models import Museum
from rest_framework import serializers, viewsets

class MuseumSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Museum
        fields = ('name', 'max_count', 'audioguide', 'accompanying_guide')