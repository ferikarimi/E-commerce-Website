from django.db import models
from Accounts.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Vendors (models.Model):
    
    CHOISE_FIELDS =[
        ('owner' , 'owner'),
        ('manager' , 'manager'),
        ('operator' , 'operator'),
    ]

    user = models.OneToOneField(User , on_delete=models.CASCADE)
    role = models.CharField(max_length=10 , choices=CHOISE_FIELDS , default='owner')
    vendor_code = models.OneToOneField('VendorCode' , on_delete=models.SET_NULL , null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self' , on_delete=models.SET_NULL , null=True , blank=True , related_name='vendor_member')
 
class VendorCode(models.Model):
    class Meta :
        ordering = ['-created_at']
        
    code = models.PositiveIntegerField(unique=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Shop (models.Model):
    vendor = models.OneToOneField(Vendors , on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone = PhoneNumberField(null=True , blank=True)
    description = models.TextField(null=True , blank=True)
    field = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True , null=True , blank=True)
    product_sold_count = models.PositiveIntegerField(default=0)