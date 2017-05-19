from django import forms
from django.forms import ModelForm
from avangard.museums.models import Museum


class MuseumForm(ModelForm):
    class Meta:
        model = Museum
        fields = ['name', 'max_count', 'audioguide', 'accompanying_guide']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'max_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'audioguide': forms.CheckboxInput(attrs={'style':'margin-right: 10px'}),
            'accompanying_guide': forms.CheckboxInput(attrs={'style':'margin-right: 10px'}),
        }
