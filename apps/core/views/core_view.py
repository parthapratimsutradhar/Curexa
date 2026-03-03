from django.views import View
from django.shortcuts import redirect, render

class EmergencyView(View):
    def get(self, request):
        return render (request, "enduser/emergency_urgent_care.html")
    
class AboutView(View):
    def get(self, request):
        return render (request, "enduser/about_curexa.html")

def not_found_page(request, path=None):
    return render(request, "extra/not_found.html", status=404)
