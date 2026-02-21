from django.db import models
from apps.core.models.base_model import BaseModel

class Cart(BaseModel):    
    owner = models.OneToOneField(
        'accounts.PatientProfile',
        on_delete=models.CASCADE, 
        related_name='fk_cart_owner_cart_ppatient_id'
    )

    class Meta:
        db_table = 'carts'

    def __str__(self):
        return f"{self.id} | User: {self.owner.get_full_name()}"

