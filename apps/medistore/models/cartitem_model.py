from django.db import models
from apps.core.models.base_model import BaseModel
from django.db.models import Q

class CartItem(BaseModel):
    medicine = models.ForeignKey(
        'medistore.Medicine', 
        on_delete=models.CASCADE, 
        related_name='fk_medicine_cart_items_medicine_id'
    )
    cart = models.ForeignKey(
        'medistore.Cart',
        on_delete=models.CASCADE, 
        related_name='fk_cart_cart_items_cart_id'
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'cart_items'
        constraints = [
            models.UniqueConstraint(
                fields=['cart', 'medicine'],
                condition=Q(is_active=True),
                name='unique_active_cart_medicine'
            )
        ]

    def __str__(self):
        return f"{self.medicine.name} | Quantity: {self.quantity} | Cart Owner: {self.cart.owner.patient.get_full_name()}"
