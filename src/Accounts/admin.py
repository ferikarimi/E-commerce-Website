from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ordering = ["username"]

    search_fields = ["username"]

    fieldsets = [
        (
            None,
            {
                "fields": [("is_vendor" , "is_customer") ,("first_name", "last_name") , ("username" , "password" , "email" , "phone_number" ,"birth_date")],
            },
        ),
    ]

    readonly_fields = ["password","last_login"]

    list_display = ["username", "is_superuser" , "is_vendor" , "is_customer"]