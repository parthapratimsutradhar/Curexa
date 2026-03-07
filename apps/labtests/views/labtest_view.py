from django.views import View
from django.shortcuts import render


class LabTestsCatalogView(View):
    def get(self, request):
        return render(request, "enduser/labtests/lab_test_catalog.html")


class TestBookingModalView(View):
    def get(self, request):
        return render(request, "enduser/labtests/test_booking_modal.html")
