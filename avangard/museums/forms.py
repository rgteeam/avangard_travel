from django import forms
from django.forms import ModelForm
from avangard.museums.models import Museum


class MuseumForm(ModelForm):
    class Meta:
        model = Museum
        fields = ['name', 'fullticket_price', 'reduceticket_price', 'audioguide_price', 'accompanying_guide_price', 'max_count']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'fullticket_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'reduceticket_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'audioguide_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'accompanying_guide_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_count': forms.NumberInput(attrs={'class': 'form-control'}),
        }
