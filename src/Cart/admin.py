from django.contrib import admin
from .models import Orders , OrderDetail

@admin.register(Orders)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(OrderDetail)
class UserAdmin(admin.ModelAdmin):
    pass