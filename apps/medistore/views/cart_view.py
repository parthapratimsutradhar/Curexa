from django.views import View
from django.shortcuts import render, redirect

class CartView(View):
    def get(self, request):
        return render(request, "enduser/medistore/cart.html")
    
class MedicineDetailsView(View):
    def get(self, request):
        return render(request, "enduser/medistore/medicine_detail.html")    