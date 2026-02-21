import hmac
import hashlib
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from apps.orders.models import Payment
from apps.core.constants.default_values import PaymentStatus

@csrf_exempt
def razorpay_webhook(request):
    payload = request.body
    signature = request.headers.get("X-Razorpay-Signature")

    expected_signature = hmac.new(
        settings.RAZORPAY_TEST_KEY_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()

    if signature != expected_signature:
        return JsonResponse({"error": "Invalid signature"}, status=400)

    data = json.loads(payload)
    event = data.get("event")

    if event == "payment.captured":
        razorpay_order_id = data["payload"]["payment"]["entity"]["order_id"]

        payment = Payment.objects.get(transaction_id=razorpay_order_id)
        payment.status = PaymentStatus.SUCCESS.value
        payment.save()

        invoice = payment.invoice
        invoice.is_paid = True
        invoice.save()

    return JsonResponse({"status": "ok"})