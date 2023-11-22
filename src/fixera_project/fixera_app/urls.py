from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('bug', views.BugSetAPIView)


urlpatterns = [
    path('', views.index_view, name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]