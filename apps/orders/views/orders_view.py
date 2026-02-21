from django.views import View
from django.shortcuts import render
from apps.accounts.services import patient_services
from apps.medistore.services import cart_services
from apps.orders.services import orders_services
from django.http import JsonResponse

class OrderListView(View):
    def get(self, request):
        return render(request, "enduser/orders/order_list.html")
    
class OrderDetailsView(View):
    def get(self, request, pk):
        return render(request, "enduser/orders/order_detail.html")


class OrderCreateView(View):
    def post(self, request):
        patient= patient_services.get_patient(request.user.id)
        
        # 1️⃣ Get cart details
        cart = cart_services.get_cart_details(patient)
        items = cart.get("items", [])

        if not items:
            return JsonResponse({"success": False, "message": "Cart is empty"}, status=400)


        # 4️⃣ Create the order
        order = orders_services.order_create(patient)
        # 5️⃣ Create order items
        orders_services.bulk_create_order_items(order, items)

        # 6️⃣ Optionally, clear the cart after order creation
        cart_services.clear_cart(patient)

        return JsonResponse({
            "success": True,
            "message": "Order created successfully",
            "order_id": order.id
        })



from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.orders.services.orders_services import checkout_cart
from decimal import Decimal, ROUND_HALF_UP



class CheckoutOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Expects payload:
        {
            "cart_items": [
                {"medicine_id": 1, "quantity": 2, "retail_price": "245.00"},
                ...
            ],
            "billing_address": "123 MG Road, Kolkata",
            "tax_rate": 12
        }
        """
        patient = patient_services.get_patient(request.user.id)
        
        cart_items = request.data.get("cart_items", [])
        billing_address = request.data.get("billing_address")
        tax_rate = Decimal(request.data.get("tax_rate", "12"))

        try:
            data = checkout_cart(patient, cart_items, billing_address, tax_rate)
            return Response({"success": True, "data": data})
        except ValueError as ve:
            return Response({"success": False, "error": str(ve)}, status=400)
        except Exception as e:
            # log exception here
            import traceback
            print(traceback.format_exc())  # temporarily
            return Response({"success": False, "error": "Checkout failed"}, status=500)        