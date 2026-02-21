from django.db import models
from apps.core.models.base_model import BaseModel
from apps.core.constants.default_values import OrderStatus

class Order(BaseModel):
    patient = models.ForeignKey(
        'accounts.PatientProfile',
        on_delete=models.CASCADE,
        related_name='fk_patient_orders_patient_id'
    )
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.IntegerField(
        choices=[(status.value, status.name) for status in OrderStatus],
        default=OrderStatus.PROCESSING.value,
    )

    class Meta:
        db_table = 'orders'
        ordering = ['-order_date']

    def __str__(self):
        return f"Order {self.id} by {self.patient.patient.get_full_name()}"
    
