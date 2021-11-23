from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-page'),
    path('evaluation/<str:output>', views.evaluation_view, name='evaluation'),
    path('feedback/<str:output>', views.feedback, name='evaluation'),
    path('API/', views.myAPI.as_view(), name='API-service'),
    path('API/<str:input>/', views.myAPISingle.as_view(), name='API-service'),
]