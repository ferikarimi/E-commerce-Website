from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Vendors , VendorCode  , Shop 



@admin.register(Vendors)
class VendorsAdmin(admin.ModelAdmin):
    search_fields = ["username"]

    list_display = ["username" , "role" , "shop_name" ,'account']

    def username (self , obj):
        return obj.user.username

    def shop_name (self, obj):
        if obj.shop:
            link = reverse("admin:Vendors_shop_change", args=[obj.shop.pk])
            return format_html('<a href="{}">{}</a>', link, obj.shop.name)
        return "-"

    def account (self, obj):
        if obj.user:
            link = reverse("admin:Accounts_user_change", args=[obj.user.pk])
            return format_html('<a href="{}">{}</a>', link, obj.user)
        return "-"
    

@admin.register(VendorCode)
class VendorCodeAdmin(admin.ModelAdmin):
    search_fields = ["is_used"]

    list_display = ["code" , "is_used"]


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    search_fields = ["name"]

    list_display = ["name" , "field"]