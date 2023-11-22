from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from .models import Bug
from .forms import BugCreationForm


def index(request):
    return render(request, 'fixera_app/index.html', {'bugs': Bug.list_all(), 'form': BugCreationForm(),})


@method_decorator(require_http_methods(['GET', 'POST']), name='dispatch')
class BugView(View):
    def get(self, request):
        return JsonResponse({'bugs': Bug.list_all()})

    def post(self, request):
        form = BugCreationForm(request.POST)
        if form.is_valid():
            bug = form.save()
            return JsonResponse(bug.serialize_to_dict(), status=201)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
