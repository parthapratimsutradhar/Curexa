from django.views import View
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from apps.orders.models import Invoice, Order
from apps.orders.services.payment_service import create_razorpay_order
from apps.accounts.services import patient_services



def initiate_payment(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id, is_paid=False)
    data = create_razorpay_order(invoice)
    return JsonResponse(data)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.orders.services.payment_service import create_razorpay_order

class CreatePaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        invoice_id = request.data.get("invoice_id")

        if not invoice_id:
            return Response({"error": "Invoice ID required"}, status=400)

        data = create_razorpay_order(invoice_id)
        return Response(data)
    
    
from django.http import JsonResponse
from apps.orders.models import Invoice

def test_razorpay_order(request):
    try:
        patient=patient_services.get_patient(2)
        order = Order.objects.create(
            patient=patient
        )

        
        invoice = Invoice.objects.create(
            patient=patient,
            content_object=order,
            invoice_number="INV172",
            subtotal=500,
            tax_amount=50,
            discount_amount=0,
            total_amount=550
        )
        data = create_razorpay_order(invoice.id)
        return JsonResponse({"success": True, "data": data})
    except Invoice.DoesNotExist:
        return JsonResponse({"success": False, "error": "Invoice not found"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)    
    
class testpage(View):
    def get(self, request):
        return render(request, "enduser/test.html")