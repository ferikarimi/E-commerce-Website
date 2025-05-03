from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import  Addresses



@admin.register(Addresses)
class AddressesAdmin(admin.ModelAdmin):
    search_fields = ["user__username"]

    list_display = ["id","users"]

    def users (self, obj):
        if obj.user:
            link = reverse("admin:Accounts_user_change", args=[obj.user.pk])
            return format_html('<a href="{}">{}</a>', link, obj.user)
        return "-"