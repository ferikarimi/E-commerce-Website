from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Category , Product , Discount , Reviews



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]

    list_display = [
        "name" , "parent"
        ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ["name"]

    list_display = ["name" , "categories"]
    
    def categories (self, obj):
        if obj.category:
            link = reverse("admin:Products_category_change", args=[obj.category.pk])
            return format_html('<a href="{}">{}</a>', link, obj.category)
        return "-"


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['product', 'amount', 'is_percentage']


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    search_fields = ["customer"]

    list_display = ["customer" , "status"]