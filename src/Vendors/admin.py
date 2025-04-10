from django.contrib import admin
from .models import Vendors , VendorCode  , Shop 


@admin.register(Vendors)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(VendorCode)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Shop)
class UserAdmin(admin.ModelAdmin):
    pass
