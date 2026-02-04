from apps.doctors import views
from django.urls import path

urlpatterns = [
    
    path('doctors/', views.DoctorListView.as_view(), name='doctor_list')
]

