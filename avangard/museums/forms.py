from django.forms import ModelForm
from avangard.museums.models import Museum


class MuseumForm(ModelForm):
    class Meta:
        model = Museum
        fields = ['name', 'max_count', 'audioguide', 'accompanying_guide']
