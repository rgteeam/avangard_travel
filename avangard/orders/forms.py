from django import forms
from django.forms import ModelForm
from .models import Order
from avangard.museums.models import Museum, Schedule


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['museum', 'seance', 'company', 'fullticket_count', 'reduceticket_count', 'audioguide', 'accompanying_guide', 'name', 'email', 'phone']
        seance = forms.ModelChoiceField(queryset=None, empty_label=None, to_field_name="seance")
        audioguide = forms.BooleanField(initial=False, required=False)
        accompanying_guide = forms.BooleanField(initial=False, required=False)
        widgets = {
            'seance': forms.Select(attrs={'class': 'form-control'}),
            'fullticket_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'reduceticket_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'audioguide': forms.CheckboxInput(attrs={'style':'margin-right: 10px'}),
            'accompanying_guide': forms.CheckboxInput(attrs={'style':'margin-right: 10px'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }