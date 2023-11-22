from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Bug


class Login(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    pass


class BugCreation(forms.ModelForm):
    class Meta:
        model = Bug
        fields = ['title', 'description']