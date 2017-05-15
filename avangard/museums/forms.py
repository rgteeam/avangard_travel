from django import forms
from django.forms import ModelForm
from avangard.museums.models import Museum

class MuseumForm(ModelForm):
    class Meta:
        model = Museum
        fields = ['name', 'max_count', 'audioguide', 'accompanying_guide']

        attrs = {
            'th': {
                'name':'Название'
            }
        }