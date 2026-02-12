from django.urls import path
from apps.docbook import views

urlpatterns = [
    # Availability
    path('availability/create/', views.AvailabilityCreateAPIView.as_view(), name='admin-availability-create'),

    # {
    # "doctor": 1,
    # "date": "2026-01-22",
    # "start_time": "14:00:00",
    # "end_time": "14:30:00"
    # }
    
    
    # Appointments
    path('appointments/book/', views.AppointmentBookAPIView.as_view(), name='admin-appointment-book'),
    path('appointments/', views.AppointmentsByDoctorAPIView.as_view(), name='api_appointments'),
    
    # {
    #  "appointment_type": 1,
    #  "availability": 12,
    #  "patient": 5,
    #  "doctor": 3,
    #  "notes": "Patient has recurring headache and mild fever"
    # }

]


  
