import uuid
from decimal import Decimal, ROUND_HALF_UP
from apps.orders.models.invoice_model import Invoice
from django.core.exceptions import ValidationError


def create_invoice(
    *,
    patient,
    order=None,
    test_booking=None,
    appointment=None,
    billing_address=None,
    subtotal=Decimal("0.00"),
    tax_rate=Decimal("0.00"),
    discount_amount=Decimal("0.00"),
):
    """
    Create an Invoice for exactly ONE of:
    - Order
    - TestBooking
    - Appointment
    """

    # 1️⃣ Enforce exactly one target (service-level safety)
    targets = [order, test_booking, appointment]
    if sum(1 for t in targets if t is not None) != 1:
        raise ValidationError(
            "Invoice must be linked to exactly ONE of: order, test_booking, appointment"
        )

    # 2️⃣ Generate invoice number
    invoice_number = f"INV-{uuid.uuid4().hex[:8].upper()}"

    # 3️⃣ Calculate tax
    tax_amount = (
        subtotal * tax_rate / Decimal("100")
    ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    # 4️⃣ Calculate total
    total_amount = (
        subtotal + tax_amount - discount_amount
    ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    # 5️⃣ Create invoice
    invoice = Invoice.objects.create(
        patient=patient,
        order=order,
        test_booking=test_booking,
        appointment=appointment,
        invoice_number=invoice_number,
        billing_address=billing_address,
        subtotal=subtotal,
        tax_amount=tax_amount,
        discount_amount=discount_amount,
        total_amount=total_amount,
    )

    return invoice