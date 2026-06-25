from django.views import View
from django.shortcuts import render
from apps.core.utilities.jwt_authentication import JWTRequiredMixin
from apps.medistore.services import cart_services, medicine_services
from apps.accounts.services import patient_services
from django.http import JsonResponse

class CartView(JWTRequiredMixin, View):
    def get(self, request):
        user_id = request.user.id
        patient=patient_services.get_patient(user_id)
        user_cart=cart_services.get_cart_details(patient)
        print(user_cart)
        return render(request, "enduser/medistore/cart.html", {"cart": user_cart})
    
    

class AddToCartView(JWTRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            # Get the patient object for the logged-in user
            patient = patient_services.get_patient(request.user.id)

            # Extract medicine ID and quantity from POST data
            medicine_id = request.POST.get('medicine')
            quantity = int(request.POST.get('quantity', 1))  # default to 1 if not provided

            if not medicine_id:
                return JsonResponse({"success": False, "message": "Medicine ID is required"}, status=400)

            # Fetch medicine object
            medicine = medicine_services.get_medicine(medicine_id)

            # Add item to cart
            cart_services.add_item(patient, medicine, quantity)

            return JsonResponse({
                "success": True,
                "message": f"{medicine.name} has been added to your cart",
                "cart_item": {
                    "medicine_id": medicine.id,
                    "name": medicine.name,
                    "price": medicine.retail_price,
                    "quantity": quantity,
                }
            })
        except medicine_services.Medicine.DoesNotExist:
            return JsonResponse({"success": False, "message": "Medicine not found"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)