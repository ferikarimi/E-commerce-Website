from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from phonenumber_field.modelfields import PhoneNumberField


class User (AbstractUser):
    class Meta:
        verbose_name_plural = "Users | کاربران"
        db_table='User'

        
    phone = PhoneNumberField(unique=True)
    birth_date = models.DateField(null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_vendor = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username}"