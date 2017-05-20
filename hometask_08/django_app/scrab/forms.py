from django import forms
from .models import Coins
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class SearchForm(forms.Form):

    search = forms.CharField(label='search', max_length=100,
                             help_text="Please enter something")

