# apps/payments/services/payment_service.py
import uuid
from django.conf import settings
from apps.core.utilities.razorpay_client import client
from apps.orders.models import Invoice, Payment
from apps.core.constants.default_values import PaymentStatus, PaymentMethod
from decimal import Decimal
from django.db import transaction


def create_razorpay_order(invoice):
    """
    Create Razorpay order for an Invoice.
    Invoice must be linked to exactly ONE of:
    - Order
    - Appointment
    - TestBooking
    """

    # 🔒 Prevent duplicate pending payments
    if Payment.objects.filter(
        invoice=invoice,
        status=PaymentStatus.PENDING.value
    ).exists():
        raise ValueError("Payment already initiated for this invoice")

    # 💰 Convert amount to paise (Decimal-safe)
    amount_paise = int(Decimal(invoice.total_amount) * 100)

    # 🧠 Identify what this invoice is for (for frontend / metadata)
    target_type = None
    target_id = None

    if invoice.order:
        target_type = "order"
        target_id = invoice.order.id
    elif invoice.appointment:
        target_type = "appointment"
        target_id = invoice.appointment.id
    elif invoice.test_booking:
        target_type = "test_booking"
        target_id = invoice.test_booking.id
    else:
        raise ValueError("Invoice is not linked to any payable entity")

    # 🔁 Atomic operation (important for payments)
    with transaction.atomic():
        razorpay_order = client.order.create({
            "amount": amount_paise,
            "currency": "INR",
            "payment_capture": 1,
            "notes": {
                "invoice_number": invoice.invoice_number,
                "target_type": target_type,
                "target_id": target_id,
            }
        })

        Payment.objects.create(
            transaction_id=razorpay_order["id"],
            invoice=invoice,
            amount=invoice.total_amount,
            payment_method=PaymentMethod.RAZORPAY.value,
            status=PaymentStatus.PENDING.value
        )

    # 📦 Frontend response
    return {
        "invoice_id": invoice.id,
        "invoice_number": invoice.invoice_number,
        "razorpay_order_id": razorpay_order["id"],
        "key_id": settings.RAZORPAY_TEST_KEY_ID,
        "amount": amount_paise,
        "currency": "INR",
        "target_type": target_type,
        "target_id": target_id,
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