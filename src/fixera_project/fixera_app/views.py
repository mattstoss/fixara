from django.shortcuts import render

def index(request):
    return render(request, 'fixera_app/index.html')
