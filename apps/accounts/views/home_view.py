from django.views import View
from django.shortcuts import render,redirect
from apps.doctors.services.doctor_services import doctor_list
import random

class HomeView(View):
    def get(self, request):
        doctors = random.sample(doctor_list(), 4)
        context={
            "doctors":doctors            
        }
        return render(request, 'enduser/home.html', context)

