from django.contrib import admin
from .models import Vendors , VendorCode  , Shop 


@admin.register(Vendors)
class VendorsAdmin(admin.ModelAdmin):
    search_fields = ["username"]

    list_display = [
        "user__username" , "role" , "shop__name"
        ]

@admin.register(VendorCode)
class VendorCodeAdmin(admin.ModelAdmin):
    search_fields = ["is_used"]

    list_display = [
        "code" , "is_used"
        ]

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    search_fields = ["name"]

    list_display = [
        "name" , "field"
        ]