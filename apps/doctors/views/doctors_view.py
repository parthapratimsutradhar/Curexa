from django.views import View
from django.shortcuts import redirect, render

class DoctorListView(View):
    def get(self, request):
        return render(request, "enduser/doctors/doctor_list.html")

class DoctorProfileView(View):
    def get(self, request, pk):
        return render(request, "enduser/doctors/doctor_profile.html")
            