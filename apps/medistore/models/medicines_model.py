from django.db import models
from apps.core.models.base_model import BaseModel
from apps.core.constants.default_values import DosageForm, AGE_GROUP

class Medicine(BaseModel):
    SKU= models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    retail_price = models.DecimalField(max_digits=10, decimal_places=2)
    medicine_images = models.JSONField(
    default=list,
    blank=True,
    null=True    
    )
    is_prescription_required = models.BooleanField(default=False)
    category = models.ForeignKey(
        'medistore.Category',
        on_delete=models.CASCADE,
        related_name='fk_category_medicines_category_id'
    )
    classification = models.IntegerField(
        choices=[(tag.value, tag.name) for tag in DosageForm],
        default=DosageForm.TABLET.value, 
        null=False, blank=False
    )
    age_group = models.IntegerField(
        choices=[(group.value, group.name) for group in AGE_GROUP],
        default=AGE_GROUP.ADULT.value, 
        null=False, blank=False
    )
    salt_composition = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    dosage_strength = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=255, blank=True, null=True)
    manufacture_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    
    class Meta:
        db_table = 'medicines'
        
    def __str__(self):
        return f"{self.name} | Retail: ₹{self.retail_price} | Active: {self.is_active}"
