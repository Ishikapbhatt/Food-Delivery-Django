from django.contrib import admin
from .models import User, Address

class AddressInline(admin.TabularInline):
    model = Address
    extra = 1

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone_number', 'first_name', 'last_name', 'is_active', 'is_staff']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email', 'phone_number', 'first_name', 'last_name']
    inlines = [AddressInline]

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'address_type', 'city', 'state', 'is_default']
    list_filter = ['address_type', 'is_default', 'city', 'state']
    search_fields = ['user__username', 'user__email', 'address_line1', 'city']