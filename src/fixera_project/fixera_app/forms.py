from django import forms

from . import models


class BugCreation(forms.ModelForm):
    class Meta:
        model = models.Bug
        fields = ['title', 'description']