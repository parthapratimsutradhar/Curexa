from django.urls import path, include
from apps.doctors import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    
    path("doctors/", views.doctor_list_api, name="doctor_list_api"),
]
