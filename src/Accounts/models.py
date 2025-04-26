from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from phonenumber_field.modelfields import PhoneNumberField


class User (AbstractUser):
    phone_number = PhoneNumberField(null=True , blank=True)
    birth_date = models.DateField(null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_vendor = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)

    class Meta:
        db_table='User'
    
    def __str__(self):
        return f"{self.username}"