# apps/payments/services/payment_service.py
import uuid
from django.conf import settings
from apps.core.utilities.razorpay_client import client
from apps.orders.models import Invoice, Payment
from apps.core.constants.default_values import PaymentStatus, PaymentMethod
from decimal import Decimal


def create_razorpay_order(invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)

    amount_paise = int(invoice.total_amount * Decimal("100"))

    razorpay_order = client.order.create({
        "amount": amount_paise,
        "currency": "INR",
        "payment_capture": 1
    })

    payment = Payment.objects.create(
        transaction_id=razorpay_order["id"],  # Razorpay order_id
        invoice=invoice,
        amount=invoice.total_amount,
        payment_method=PaymentMethod.RAZORPAY.value,
        status=PaymentStatus.PENDING.value
    )

    return {
        "razorpay_order_id": razorpay_order["id"],
        "razorpay_key": settings.RAZORPAY_TEST_KEY_ID,
        "amount": amount_paise,
        "currency": "INR",
        "invoice_number": invoice.invoice_number
    } 
   


# apps/payments/views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import razorpay
from apps.orders.models import Payment
from apps.core.constants.default_values import PaymentStatus


@csrf_exempt
def verify_payment(request):
    data = request.POST
    client = razorpay.Client(
        auth=(settings.RAZORPAY_TEST_KEY_ID, settings.RAZORPAY_TEST_KEY_SECRET)
    )

    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": data["razorpay_order_id"],
            "razorpay_payment_id": data["razorpay_payment_id"],
            "razorpay_signature": data["razorpay_signature"],
        })

        payment = Payment.objects.get(transaction_id=data["razorpay_order_id"])
        payment.status = PaymentStatus.SUCCESS.value
        payment.save()

        invoice = payment.invoice
        invoice.is_paid = True
        invoice.save()

        return JsonResponse({"status": "success"})

    except razorpay.errors.SignatureVerificationError:
        return JsonResponse({"status": "failed"}, status=400)    