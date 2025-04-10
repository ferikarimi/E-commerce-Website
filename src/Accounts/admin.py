from django.contrib import admin
from .models import Customers

@admin.register(Customers)
class UserAdmin(admin.ModelAdmin):
    pass