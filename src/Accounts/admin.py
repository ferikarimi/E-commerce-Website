from django.contrib import admin
from .models import User
import jdatetime



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ordering = ["username"]

    search_fields = ["username"]

    fieldsets = [
        ("Basic Information", {
            "fields": [
                ("is_vendor", "is_customer"),
                ("first_name", "last_name"),
                ("username", "email"),
                ("phone", "birth_date"),
            ],
            "classes": ["wide"],
        }),
        ("Advanced Information", {
            "fields": [
                ("is_staff","is_superuser"),
                "is_active","date_joined_shamsi",
                "last_login_shamsi",
                  
            ],
            "classes": ["collapse"],
        }),
    ]

    list_display = ["username", "is_superuser" , "is_vendor" , "is_customer"]

    readonly_fields = ["date_joined_shamsi", "last_login_shamsi"]

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get("password"):
            obj.set_password(form.cleaned_data["password"])
        return super().save_model(request, obj, form, change)

    def date_joined_shamsi (self , obj):
        if obj.created_at :
            created_at = obj.created_at
            jalili_data = jdatetime.datetime.fromgregorian(datetime=created_at)
            return jalili_data.strftime('%Y/%m/%d')
        return None

    def last_login_shamsi (self , obj):
        if obj.last_login :
            created_at = obj.last_login
            jalili_data = jdatetime.datetime.fromgregorian(datetime=created_at)
            return jalili_data.strftime('%Y/%m/%d')
        return None