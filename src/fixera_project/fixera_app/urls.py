from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/bugs/", views.BugView.as_view(), name="api_bugs"),
]