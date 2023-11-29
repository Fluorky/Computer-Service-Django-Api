# computerserviceapp/serializers.py

from rest_framework import serializers
from .models import ServiceRequest, Invoice, Part, ServiceTechnician, Customer

class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = '__all__'

class ServiceTechnicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceTechnician
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

