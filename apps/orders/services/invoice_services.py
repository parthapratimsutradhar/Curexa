import uuid
from decimal import Decimal, ROUND_HALF_UP
from django.contrib.contenttypes.models import ContentType
from apps.orders.models.invoice_model import Invoice

def create_invoice(
    patient,
    content_object,
    billing_address=None,
    subtotal=Decimal("0.00"),
    tax_rate=Decimal("0.00"),
    discount_amount=Decimal("0.00")
):
    """
    Create an Invoice for any object (Order, TestBooking, Appointment, etc.)

    Args:
        patient: PatientProfile instance
        content_object: Order, TestBooking, Appointment, etc.
        billing_address: Optional billing address
        subtotal: Decimal, total before tax & discount
        tax_rate: Decimal, percentage of tax (e.g., 12 for 12%)
        discount_amount: Decimal, fixed discount

    Returns:
        Invoice instance
    """

    # Generate a unique invoice number (example: INV-20260221-UUID4)
    invoice_number = f"INV-{uuid.uuid4().hex[:8].upper()}"

    # Calculate tax amount
    tax_amount = (subtotal * tax_rate / 100).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    # Calculate total
    total_amount = (subtotal + tax_amount - discount_amount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    # Create the invoice
    invoice = Invoice.objects.create(
        patient=patient,
        content_object=content_object,
        invoice_number=invoice_number,
        billing_address=billing_address,
        subtotal=subtotal,
        tax_amount=tax_amount,
        discount_amount=discount_amount,
        total_amount=total_amount,
    )

    return invoice