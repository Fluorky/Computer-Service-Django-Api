from .models import Part, ServiceRequest, Invoice, Customer
# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ServiceTechnician


class CustomUserAdmin(UserAdmin):
    model = ServiceTechnician
    list_display = ['id', 'email', 'specialization', 'is_staff', 'is_superuser']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('specialization',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(ServiceTechnician, CustomUserAdmin)
admin.site.register(Part)
admin.site.register(ServiceRequest)
admin.site.register(Invoice)
admin.site.register(Customer)
