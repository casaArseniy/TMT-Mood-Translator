from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-page'),
    path('evaluation/<str:output>', views.evaluation_view, name='evaluation'),
    path('feedback/<str:output>', views.feedback, name='evaluation'),
    path('API/analysis/', views.all_API_analysis.as_view(), name='API-service'),
    path('API/feedback/', views.all_API_feedback.as_view(), name='API-service'),
    path('API/analysis/<str:my_input>', views.myAPI_analysis.as_view(), name='API-service'),
    path('API/feedback/<str:my_input>/', views.myAPIS_feedback.as_view(), name='API-service'),
]
