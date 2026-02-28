from django.db import models
from apps.core.models.base_model import BaseModel
from apps.core.constants.default_values import AppointmentType, AppointmentStatus

class Appointment(BaseModel):
    appointment_type = models.IntegerField(
        choices=[(t.value, t.name) for t in AppointmentType],
        default=AppointmentType.CONSULTATION.value
    )

    availability = models.OneToOneField(
        "docbook.Availability",
        on_delete=models.CASCADE,
        related_name='fk_availability_appointment_availability_id'
    )

    appointment_status = models.IntegerField(
        choices=[(s.value, s.name) for s in AppointmentStatus],
        default=AppointmentStatus.SCHEDULED.value
    )

    patient = models.ForeignKey(
        'accounts.PatientProfile',
        on_delete=models.CASCADE,
        related_name='fk_patient_appointment_patient_id'
    )

    doctor = models.ForeignKey(
        'doctors.DoctorProfile',
        on_delete=models.CASCADE,
        related_name='fk_doctor_appointments_doctor_id'
    )

    base_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )

    tax_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )

    total_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'appointments'
        ordering = ['availability__date', 'availability__start_time']

    def __str__(self):
        return f"{self.patient.get_full_name()} → {self.doctor.get_full_name()} ({self.availability})"
