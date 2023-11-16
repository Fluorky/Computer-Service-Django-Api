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

class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = '__all__'

class ServiceTechnician(forms.ModelForm):
    class Meta:
        model = ServiceTechnician
        fields = '__all__'

class Customer(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'



# ...

