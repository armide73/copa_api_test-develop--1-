from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from .models import User


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'names', 'phone_number']
    fieldsets = (
        (None, {
            'fields': (
                'email', 'password', 'keywords'
            ),
        }),
        (_('Personal Info'), {
            'fields': (
                'names',
            )
        }),
        (_('Permittions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser'
            )
        }),
        (_('Important dates'), {
            'fields': (
                'last_login',
            )
        })
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2')
        }),
    )


admin.site.register(User, UserAdmin)
