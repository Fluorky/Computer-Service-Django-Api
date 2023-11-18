from django.contrib import admin
from . models import Part, ServiceRequest, ServiceTechnician, Invoice, Customer


# Register your models here.

admin.site.register(Part)
admin.site.register(ServiceTechnician)
admin.site.register(ServiceRequest)
admin.site.register(Invoice)
admin.site.register(Customer)
