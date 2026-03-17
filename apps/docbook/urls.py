from apps.docbook import views
from django.urls import path

urlpatterns = [
    path('appointments/', views.AppointmentsListView.as_view(), name='appointments'),
    path('appointments/book/', views.AppointmentBookView.as_view(), name='appointment_book'),
    path('appointments/check-prescription/', views.CheckPrescriptionView.as_view(), name='check_prescription'),
    
]

