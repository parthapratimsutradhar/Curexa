from django.http import JsonResponse   
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
import razorpay
from apps.core.utilities.razorpay_client import client

@csrf_exempt
def verify_razorpay_payment(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    data = json.loads(request.body)

    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": data["razorpay_order_id"],
            "razorpay_payment_id": data["razorpay_payment_id"],
            "razorpay_signature": data["razorpay_signature"],
        })

        return JsonResponse({"success": True})

    except razorpay.errors.SignatureVerificationError:
        return JsonResponse({"success": False}, status=400)