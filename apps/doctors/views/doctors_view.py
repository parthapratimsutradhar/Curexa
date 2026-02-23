from django.views import View
from django.shortcuts import redirect, render
from apps.doctors.services import doctor_services
class DoctorListView(View):
    def get(self, request):
        doctors = doctor_services.doctor_list()
        return render(request, "enduser/doctors/doctor_list.html", {"doctors":doctors})

class DoctorProfileView(View):
    def get(self, request, pk):
        return render(request, "enduser/doctors/doctor_profile.html")
            