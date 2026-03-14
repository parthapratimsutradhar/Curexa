from django.views import View
from django.shortcuts import render,redirect
from apps.doctors.services.doctor_services import doctor_list

class HomeView(View):
    def get(self, request):
        doctors = doctor_list()
        context={
            "doctors":doctors            
        }
        return render(request, 'enduser/home.html', context)

