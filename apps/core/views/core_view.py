from django.views import View
from django.shortcuts import redirect, render

from apps.core.utilities.route_collector import build_route_docs_context


class RouteDocumentationView(View):
    def get(self, request):
        context = build_route_docs_context()
        return render(request, "docs/route_documentation.html", context)


class EmergencyView(View):
    def get(self, request):
        return render (request, "enduser/emergency_urgent_care.html")
    
class AboutView(View):
    def get(self, request):
        return render (request, "enduser/about_curexa.html")

def not_found_page(request, path=None):
    return render(request, "extra/not_found.html", status=404)
