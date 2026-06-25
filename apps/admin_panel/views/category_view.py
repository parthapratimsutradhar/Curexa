from django.views import View
from django.shortcuts import render, redirect

class CategoryListView(View):
    def get(self, request):
        
        return render(request, "admin/catagories/catagories_list.html")
    
class InventoryListView(View):
    def get(self, request):
        
        return render(request, "admin/medicens/medicens_inventory.html")    