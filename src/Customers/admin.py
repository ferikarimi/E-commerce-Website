from django.contrib import admin
from .models import  Addresses

@admin.register(Addresses)
class AddressesAdmin(admin.ModelAdmin):
    search_fields = ["user__username"]

    list_display = ["user"]