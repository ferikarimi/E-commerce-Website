from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from phonenumber_field.modelfields import PhoneNumberField


class Customers (AbstractUser):
    email = models.CharField(unique=True)
    phone_number = PhoneNumberField(null=True , blank=True) # بعدا اجباری میشه تو فاز های بعدی
    birth_date = models.DateField(null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True , blank=True)
    is_vendor = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)

    class Meta:
        db_table='customers'
    
    def __str__(self):
        return f"{self.username}"