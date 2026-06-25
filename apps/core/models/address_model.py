from django.db import models

class AddressModel(models.Model):
       
    house_number = models.CharField(max_length=100, null=True, blank=True)   
    street = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    pin_code = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    
    is_default = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        abstract = True
