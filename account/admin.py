from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from rest_framework.authtoken.admin import TokenAdmin


class AccountAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'date_of_birth', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

TokenAdmin.raw_id_fields = ['user']

admin.site.register(User, AccountAdmin)
