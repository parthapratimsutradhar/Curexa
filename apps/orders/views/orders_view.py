from django.views import View
from django.shortcuts import render

class OrderListView(View):
    def get(self, request):
        return render(request, "enduser/orders/order_list.html")
    
class OrderDetailsView(View):
    def get(self, request, pk):
        return render(request, "enduser/orders/order_detail.html")
