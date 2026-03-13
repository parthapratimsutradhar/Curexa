from django.db import models
from apps.core.models.address_model import AddressModel

class DoctorProfile(AddressModel):
    doctor = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='fk_doctor_doctor_profile_user_id'
    )
    specialization = models.ForeignKey(
        'doctors.Specialization',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fk_specialization_doctor_profile_specialization_id'
    )
    clinic_address = models.CharField(max_length=255, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    experience_years = models.PositiveIntegerField()
    license_number = models.CharField(max_length=50)
    license_expiry = models.DateField(blank=True, null=True)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.JSONField(
        default=list,
        blank=True,
        null=True
    )
    bio = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'doctors'
        ordering = ['doctor__first_name']
    
    def __str__(self):
        return f"Doctor: {self.doctor.get_full_name()} | Specialization: {self.specialization} | Active: {self.doctor.is_active}"
