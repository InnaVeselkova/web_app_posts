from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('login', 'email', 'first_name', 'last_name', 'phone_number', 'birth_date', 'created_at')
    list_filter = ('created_at', 'birth_date', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('login', 'email', 'first_name', 'last_name', 'phone_number')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    fieldsets = (
        ('Логин и пароль', {
            'fields': ('login', 'password')
        }),
        ('Личная информация', {
            'fields': ('username', 'email', 'first_name', 'last_name', 'phone_number', 'birth_date')
        }),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Важные даты', {
            'fields': ('last_login', 'created_at', 'updated_at')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('login', 'password1', 'password2'),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        """Пароль нельзя редактировать напрямую через админку"""
        if obj:
            return self.readonly_fields + ('password',)
        return self.readonly_fields
