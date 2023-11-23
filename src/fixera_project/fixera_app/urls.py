from django.urls import include, path
from rest_framework.routers import DefaultRouter
from django.contrib.auth.views import LogoutView

from . import views


router = DefaultRouter()
router.register('bug', views.BugSetAPIView)


urlpatterns = [
    path('', views.index_view, name='index'),
    path('login/', views.FixeraLoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]