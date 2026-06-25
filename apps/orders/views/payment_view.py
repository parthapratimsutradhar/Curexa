import json

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

import razorpay

from apps.orders.models import Payment
from apps.core.constants.default_values import PaymentStatus, AppointmentStatus, OrderStatus
from apps.core.utilities.razorpay_client import client


@csrf_exempt
def verify_razorpay_payment(request):
    """
    Verify Razorpay payment signature and update the full payment lifecycle:
    - Payment  → SUCCESS
    - Invoice  → is_paid = True
    - Appointment → CONFIRMED  (if linked to an appointment)
    - Order       → PROCESSING remains; set to SHIPPED by fulfilment team
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({"error": "Invalid JSON body"}, status=400)

    required_fields = ("razorpay_order_id", "razorpay_payment_id", "razorpay_signature")
    missing = [f for f in required_fields if not data.get(f)]
    if missing:
        return JsonResponse({"error": f"Missing fields: {', '.join(missing)}"}, status=400)

    try:
        # 1️⃣ Verify Razorpay signature
        client.utility.verify_payment_signature({
            "razorpay_order_id": data["razorpay_order_id"],
            "razorpay_payment_id": data["razorpay_payment_id"],
            "razorpay_signature": data["razorpay_signature"],
        })
    except razorpay.errors.SignatureVerificationError:
        return JsonResponse({"error": "Invalid payment signature"}, status=400)

    try:
        payment = Payment.objects.select_related(
            "invoice",
            "invoice__order",
            "invoice__appointment",
            "invoice__test_booking",
        ).get(transaction_id=data["razorpay_order_id"])
    except Payment.DoesNotExist:
        return JsonResponse({"error": "Payment record not found"}, status=404)

    if payment.status == PaymentStatus.SUCCESS.value:
        return JsonResponse({"status": "already_verified"}, status=200)

    with transaction.atomic():
        # 2️⃣ Mark payment as successful
        payment.status = PaymentStatus.SUCCESS.value
        payment.save(update_fields=["status", "updated_at"])

        # 3️⃣ Mark invoice as paid
        invoice = payment.invoice
        invoice.is_paid = True
        invoice.save(update_fields=["is_paid", "updated_at"])

        # 4️⃣ Propagate status to the linked entity
        if invoice.appointment:
            invoice.appointment.appointment_status = AppointmentStatus.CONFIRMED.value
            invoice.appointment.save(update_fields=["appointment_status", "updated_at"])

        elif invoice.order:
            # Order stays in PROCESSING until dispatched; no status change needed here.
            pass

        elif invoice.test_booking:
            # TestBooking is acknowledged; lab fulfilment manages status separately.
            pass

    return JsonResponse({"status": "success", "message": "Payment verified successfully"})