from django.contrib import admin
from .models import  Addresses

@admin.register(Addresses)
class UserAdmin(admin.ModelAdmin):
    pass