from apps.doctors import views
from django.urls import path

urlpatterns = [
    path('doctor/login/', views.DoctorLoginView.as_view(), name='doctor_login'),
    path('doctor/logout/', views.DoctorLogoutView.as_view(), name='doctor_logout'),
    path('doctor/profile/', views.DoctorPortalProfileView.as_view(), name='doctor_profile'),
    path('doctor/appointments/', views.DoctorAppointmentManagementView.as_view(), name='doctor_appointment_management'),
    path('doctor/availability/', views.DoctorAvailabilityManagementView.as_view(), name='doctor_availability_management'),
    path('doctor/earnings/', views.DoctorEarningView.as_view(), name='doctor_earning'),
    path('doctor/prescription/', views.DoctorPrescriptionView.as_view(), name='doctor_prescription'),
    path('doctor/<int:pk>/profile', views.DoctorProfileView.as_view(), name='doctor_profilr')
]
