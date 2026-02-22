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


# /////////////////////////////////////////////////////////////// API VIEWs \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response



class CheckoutOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        patient = patient_services.get_patient(request.user.id)
        cart_items = cart_services.get_cart_item(patient)

        try:
            payment_payload = orders_services.checkout_cart(patient, cart_items)

            return Response({
                "success": True,
                "data": {
                    "payment": payment_payload,
                    "customer_name": patient.patient.get_full_name(),
                    "customer_email": patient.patient.email
                }
            })

        except ValueError as ve:
            return Response({"success": False, "error": str(ve)}, status=400)
        except Exception:
            import traceback
            print(traceback.format_exc())
            return Response({"success": False, "error": "Checkout failed"}, status=500)