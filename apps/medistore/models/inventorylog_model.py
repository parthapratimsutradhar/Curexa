from django.db import models
from apps.core.constants.default_values import InventoryAction
from apps.core.models.base_model import BaseModel

class InventoryLog(BaseModel):
    medicine = models.ForeignKey(
        'medistore.Medicine',
        on_delete=models.CASCADE, 
        related_name='fk_inventory_logs_medicine_medicine_id'
    )
    quantity_change = models.PositiveIntegerField(default=0)
    action = models.IntegerField(
        choices=[(action.value, action.name) for action in InventoryAction],
        null=False, blank=False
    )
    performed_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fk_inventory_logs_users_user_id',
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'inventory_logs'

    def __str__(self):
        return f"{self.medicine.name} | Action: {self.action} | Quantity: {self.quantity} | Time: {self.timestamp}"