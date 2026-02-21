from django.views import View
from django.shortcuts import redirect, render

class InvoiceCreateView(View):
    def post(self, request):
        return