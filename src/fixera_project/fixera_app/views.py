from django.shortcuts import render, redirect
from django.views import View
from rest_framework import viewsets
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from . import models
from . import serializers 
from . import forms
from . import auth


_HOMEPAGE = 'index'


@login_required
def index_view(request):
    return render(request, 'fixera_app/index.html', {'bugs': models.Bug.get_all(), 'form': forms.BugCreation(),})


@login_required
def logout_view(request):
    auth.do_logout(request)
    return redirect('login')
    

@method_decorator(require_http_methods(['GET', 'POST']), name='dispatch')
class LoginView(View):
    @staticmethod
    def _render(request, login_form):
        return render(request, 'fixera_app/login.html', {'login_form': login_form})

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(_HOMEPAGE)
        return LoginView._render(request, forms.Login())

    def post(self, request):
        form = forms.Login(request.POST)
        if not form.is_valid():
            return LoginView._render(request, form)

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = auth.do_login(request, username, password)
        if not user:
            form.add_error(None, 'Invalid login credentials. Please try again.')
            return LoginView._render(request, form)

        return redirect(_HOMEPAGE)


@method_decorator(require_http_methods(['GET', 'POST']), name='dispatch')
class RegisterView(View):
    @staticmethod
    def _render(request, register_form):
        return render(request, 'fixera_app/register.html', {'register_form': register_form})

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(_HOMEPAGE)
        return RegisterView._render(request, forms.RegisterForm())

    def post(self, request):
        form = forms.RegisterForm(request.POST)
        if not form.is_valid():
            return RegisterView._render(request, form)

        _ = form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = auth.do_login(request, username, password)
        if not user:
            form.add_error(None, 'Registration succeeded but subsequent login failed. This should never happen')
            return RegisterView._render(request, form)

        return redirect(_HOMEPAGE)


class BugSetAPIView(viewsets.ModelViewSet):
    queryset = models.Bug.get_all()
    serializer_class = serializers.Bug
