from django.contrib import admin
from .models import Orders , OrderDetail

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    ordering = ["total_price"]

    search_fields = ["status"]

    list_display = ["customer" , "status" , "total_price"]


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    search_fields = ["order"]

    list_display = ["order__id" , 'product__name' , 'quantity']