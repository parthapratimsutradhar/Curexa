from apps.labtests import views
from django.urls import path

urlpatterns = [
    path('lab-tests/', views.LabTestsCatalogView.as_view(), name='labtests_catalog'),
    path('lab-tests/book/', views.TestBookingModalView.as_view(), name='labtests_booking_modal'),
]

