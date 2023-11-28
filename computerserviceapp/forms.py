from django import forms
from .models import ServiceRequest, Invoice, Part, ServiceTechnician, Customer

class ServiceRequestForm(forms.ModelForm):
    class Meta:

        
        model = ServiceRequest
        fields = '__all__'
  
        #owned_by = forms.ModelChoiceField(queryset=ServiceTechnician.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
        #requested_by = forms.ModelChoiceField(queryset=Customer.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
       


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'

class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = '__all__'

class ServiceTechnicianForm(forms.ModelForm):
    class Meta:
        model = ServiceTechnician
        fields = '__all__'

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'



# ...

