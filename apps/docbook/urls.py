from apps.docbook import views
from django.urls import path

urlpatterns = [
    path('appointments/', views.AppointmentsListView.as_view(), name='appointments')
    
]

