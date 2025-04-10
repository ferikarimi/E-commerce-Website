from django.db import models
from Accounts.models import Customers
from phonenumber_field.modelfields import PhoneNumberField


class Vendors (models.Model):
    
    CHOISE_FIELDS =[
        ('owner' , 'owner'),
        ('manager' , 'manager'),
        ('operator' , 'operator')
    ]

    user = models.OneToOneField(Customers , on_delete=models.CASCADE)
    role = models.CharField(max_length=10 , choices=CHOISE_FIELDS , default='owner')
    vendor_code = models.OneToOneField('VendorCode' , on_delete=models.SET_NULL , null=True , blank=True)
    phone_number = PhoneNumberField(null=True , blank=True)  # بعدا اجباری میشه تو فاز های بعدی
    birth_date = models.DateField(null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True , blank=True)
    is_vendor = models.BooleanField(default=True)
    is_customer = models.BooleanField(default=False)

 
class VendorCode(models.Model):
    code = models.PositiveIntegerField(unique=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Shop (models.Model):
    vendor = models.OneToOneField(Vendors , on_delete=models.CASCADE , related_name='shops')
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone = PhoneNumberField(null=True , blank=True)
    description = models.TextField(null=True , blank=True)