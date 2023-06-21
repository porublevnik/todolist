from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from core.models import User

@admin.register(User)
class CustomAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Dpecial dates', {'fields': ('last_login', 'date_joined')})
    )

admin.site.unregister(Group)
