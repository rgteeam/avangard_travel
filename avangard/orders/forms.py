from django import forms
from django.forms import ModelForm
from .models import Order
from avangard.museums.models import Museum, Schedule


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['museum', 'seance', 'fullticket_count', 'reduceticket_count', 'audioguide', 'accompanying_guide',
                  'name', 'email', 'phone']
        seance = forms.ModelChoiceField(queryset=None, empty_label=None, to_field_name="seance")
        audioguide = forms.BooleanField(initial=False, required=False)
        fullticket_count = forms.DecimalField(required=True, min_value=0)
        reduceticket_count = forms.DecimalField(required=True, min_value=0)
        accompanying_guide = forms.BooleanField(initial=False, required=False)
        widgets = {
            'seance': forms.Select(attrs={'class': 'form-control'}),
            'fullticket_count': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'reduceticket_count': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'accompanying_guide': forms.CheckboxInput(attrs={'style': 'margin-right: 10px'}),
            'audioguide': forms.CheckboxInput(attrs={'style': 'margin-right: 10px'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_fullticket_count(self):
        data = self.cleaned_data['fullticket_count']
        seance = self.cleaned_data['seance']

        if seance.full_count < int(data):
            raise forms.ValidationError(
                "Недостаточно взрослых билетов для совершения заказа (Доступно: %s)" % seance.full_count)
        return data

    def clean_reduceticket_count(self):
        data = self.cleaned_data['reduceticket_count']
        seance = self.cleaned_data['seance']

        if seance.reduce_count < int(data):
            raise forms.ValidationError(
                "Недостаточно льготных билетов для совершения заказа (Доступно: %s)" % seance.reduce_count)
        return data

    def clean(self):
        cleaned_data = super(OrderForm, self).clean()
        if 'fullticket_count' in cleaned_data and 'reduceticket_count' in cleaned_data:
            fullticket_count = int(cleaned_data['fullticket_count'])
            reduceticket_count = int(cleaned_data['reduceticket_count'])
            seance = cleaned_data.get("seance")

            if fullticket_count + reduceticket_count > int(seance.museum.max_count):
                raise forms.ValidationError(
                    "Максимальная численность группы %s человек" % seance.museum.max_count)
