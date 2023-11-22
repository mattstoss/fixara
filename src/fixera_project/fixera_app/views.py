from django.shortcuts import render
from rest_framework import viewsets

from .models import Bug
from .serializers import BugSerializer 
from .forms import BugCreationForm


def index(request):
    return render(request, 'fixera_app/index.html', {'bugs': Bug.get_all(), 'form': BugCreationForm(),})


class BugViewSet(viewsets.ModelViewSet):
    queryset = Bug.get_all()
    serializer_class = BugSerializer
