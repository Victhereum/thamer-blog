from django import forms
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.ModelForm):
    username = forms.CharField(label='username')
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='First name')
    last_name = forms.CharField(label='Last name')
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image',)