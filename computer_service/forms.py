from django import forms
from .models import ServiceRequest, Invoice, Part, ServiceTechnician, Customer

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = '__all__'

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'

##TO DO##
# Similar forms for Part, ServiceTechnician, and Customer

# ...

