from django.shortcuts import render, redirect
from django.views import generic
from rest_framework import viewsets
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from . import models
from . import serializers 
from . import forms
from . import auth


@login_required
def index_view(request):
    return render(request, 'fixera_app/index.html', {'bugs': models.Bug.get_all(), 'form': forms.BugCreation(),})


class _RedirectIfAuthenticatedMixin:
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().get(request, *args, **kwargs)


class FixeraLoginView(_RedirectIfAuthenticatedMixin, LoginView):
    template_name = 'fixera_app/login.html'


class RegisterView(_RedirectIfAuthenticatedMixin, generic.CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'fixera_app/register.html'

    def form_valid(self, form):
        form.save()
    
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        if not auth.do_login(self.request, username, password):
            form.add_error(None, 'Registration succeeded but subsequent login failed. This should never happen')
            return RegisterView._render(self.request, form)
        
        return self.get(self.request)


class BugSetAPIView(viewsets.ModelViewSet):
    queryset = models.Bug.get_all()
    serializer_class = serializers.Bug
