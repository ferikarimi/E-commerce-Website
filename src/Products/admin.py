from django.contrib import admin
from .models import Category , Product , Discount , Reviews

# Register your models here.

@admin.register(Category)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Product)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Discount)
class UserAdmin(admin.ModelAdmin):
    list_display = ('product', 'amount', 'is_percentage')

@admin.register(Reviews)
class UserAdmin(admin.ModelAdmin):
    pass
