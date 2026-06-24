from django.views import View
from django.shortcuts import render,redirect
from apps.doctors.services.doctor_services import doctor_list
import random

class HomeView(View):
    def get(self, request):
        doctors_data = doctor_list()
        if len(doctors_data) >= 4:
            doctors = random.sample(doctors_data, 4)
        else:
            doctors = doctors_data
        context={
            "doctors":doctors            
        }
        return render(request, 'enduser/home.html', context)

