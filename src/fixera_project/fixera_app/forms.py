from django import forms
from .models import Bug


class BugCreationForm(forms.ModelForm):
    class Meta:
        model = Bug
        fields = ['title', 'description']