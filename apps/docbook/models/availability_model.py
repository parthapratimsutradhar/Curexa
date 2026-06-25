from django.db import models
from apps.core.models.base_model import BaseModel
from apps.core.constants.default_values import DAYS_OF_WEEK
from django.db.models import Q

class Availability(BaseModel):
    doctor = models.ForeignKey(
        'doctors.DoctorProfile',
        on_delete=models.CASCADE,
        related_name='fk_doctor_availabilities_doctor_id'
    )

    date = models.DateField(db_index=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    is_leave = models.BooleanField(default=False)

    class Meta:
        db_table = 'availabilities'
        unique_together = ('doctor', 'date', 'start_time')
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'date'],
                condition=Q(is_leave=True),
                name='unique_doctor_day_leave'
            )
        ]
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.doctor.doctor.get_full_name()} | {self.date} {self.start_time}-{self.end_time}"
