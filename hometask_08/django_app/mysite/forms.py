from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserForm(forms.ModelForm):
    username = forms.CharField(
        required=True,
        label='Username',
        min_length=3,
        max_length=32,
        widget=forms.TextInput(attrs={'name': 'username', 'placeholder': 'Username'})
    )
    email = forms.CharField(
        required=True,
        label='Email',
        max_length=32,
        widget=forms.TextInput(
            attrs={'type': 'email', 'name': 'email', 'placeholder': 'email'})
    )
    password = forms.CharField(
        required=True,
        label='Password',
        min_length=8,
        max_length=32,
        widget=forms.TextInput(
            attrs={'type': 'password', 'name': 'password', 'placeholder': 'Password'})
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if (username is not None) and (password) and (email):
            self.user_cache = authenticate(username=username, pw_hash=password)
            if self.user_cache:
                del self.cleaned_data['password']
                raise forms.ValidationError('User already exists')
            else:
                try:
                    User.objects.get(email=email)
                    raise forms.ValidationError('This email address is already in use.')
                except User.DoesNotExist:
                    return self.cleaned_data
        return False

    # class Meta:
    #     model = User
    #     fields = ('username', 'email', 'password')
