from django.contrib import admin
from .models import Category , Product , Discount , Reviews

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]

    list_display = [
        "name" , "parent"
        ]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ["name"]

    list_display = [
        "name" , "category"
        ]

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('product', 'amount', 'is_percentage')

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    search_fields = ["customer"]

    list_display = [
        "customer" , "status"
        ]