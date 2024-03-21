from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model


from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.search_fields = ['user__username']

User = get_user_model()
search_fields = ('email',)
# class CustomUserAdmin(UserAdmin):
    # list_display = ('phone','email', 'is_varified', 'is_staff', 'is_superuser','is_active')
    # list_filter = ('is_varified', 'is_staff', 'is_superuser')
    # fieldsets = (
    #     (None, {'fields': ('email', 'password')}),
    #     ('Permissions', {'fields': ('is_varified', 'is_staff', 'is_superuser','is_active','groups')}),
    # )
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('email','phone', 'password1', 'password2', 'is_varified','is_active', 'is_staff', 'is_superuser','groups'),
    #     }),
    # )

    # ordering = ('email',)
    # filter_horizontal = ()


admin.site.register(User)