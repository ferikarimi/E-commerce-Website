from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Orders , OrderDetail



@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    ordering = ["total_price"]

    search_fields = ["customer" ,"status"]

    list_display = ["id" ,"customers" , "status" , "total_price"]

    def customers (self, obj):
        if obj.customer:
            link = reverse("admin:Accounts_user_change", args=[obj.customer.pk])
            return format_html('<a href="{}">{}</a>', link, obj.customer)
        return "-"


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    search_fields = ["id"]

    list_display = ["id","orders" , 'product__name' , 'quantity','vendor']

    def orders (self, obj):
        if obj.order:
            link = reverse("admin:Cart_orders_change", args=[obj.order.pk])
            return format_html('<a href="{}">{}</a>', link, obj.order)
        return "-"