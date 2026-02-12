from apps.core import views
from django.urls import path

urlpatterns = [
    
    path('emergency/', views.EmergencyView.as_view(), name='emergency_care'),
    path('about/', views.AboutView.as_view(), name='about'),

]

