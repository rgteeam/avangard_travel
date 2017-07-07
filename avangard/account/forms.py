from django.contrib.auth.forms import AuthenticationForm
from django import forms

# If you don't do this you cannot use Bootstrap CSS
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.TextInput(attrs={'type':'password','class': 'form-control', 'name': 'password', 'id':'password'}))

class SignupForm(forms.Form):

    phone = forms.CharField(max_length=30, label='phone')

    def signup(self, request, user):
        user.phone = self.cleaned_data['phone']
        user.save()