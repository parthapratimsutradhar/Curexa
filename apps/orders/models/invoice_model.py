from django.db import models
from apps.core.models.base_model import BaseModel
from django.db.models import Q


class Invoice(BaseModel):
    patient = models.ForeignKey(
        'accounts.PatientProfile',
        on_delete=models.CASCADE,
        related_name='fk_patient_invoices_patient_id'
    )

    order = models.OneToOneField(
        'orders.Order',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='fk_order_invoices_order_id'
    )

    test_booking = models.OneToOneField(
        'labtests.TestBooking',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='fk_test_booking_invoices_test_booking_id'
    )

    appointment = models.OneToOneField(
        'docbook.Appointment',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='fk_appointment_invoices_appointment_id'
    )
    invoice_number = models.CharField(max_length=20, unique=True)
    billing_address = models.TextField(null=True, blank=True)

    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    issued_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    class Meta:
        db_table = 'invoices'
        ordering = ['-issued_at']
        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(order__isnull=False, test_booking__isnull=True, appointment__isnull=True) |
                    Q(order__isnull=True, test_booking__isnull=False, appointment__isnull=True) |
                    Q(order__isnull=True, test_booking__isnull=True, appointment__isnull=False)
                ),
                name="invoice_exactly_one_target"
            )
        ]

    def __str__(self):
        if self.order:
            return f"Invoice #{self.invoice_number} for Order #{self.order.id}"
        if self.test_booking:
            return f"Invoice #{self.invoice_number} for TestBooking #{self.test_booking.id}"
        if self.appointment:
            return f"Invoice #{self.invoice_number} for Appointment #{self.appointment.id}"
        return f"Invoice #{self.invoice_number}"
