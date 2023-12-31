# computerserviceapp/serializers.py

from rest_framework import serializers
from .models import ServiceRequest, Invoice, Part, ServiceTechnician, Customer, RepairLog, Warehouse

class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = '__all__'


class InvoiceSerializer(serializers.ModelSerializer):
    service_requests = serializers.PrimaryKeyRelatedField(queryset=ServiceRequest.objects.all(), many=True)
    parts = serializers.PrimaryKeyRelatedField(queryset=Part.objects.all(), many=True)
    total_tax = serializers.SerializerMethodField()
    total_amount_with_tax = serializers.SerializerMethodField()
    total_amount_without_tax = serializers.SerializerMethodField()
    
    class Meta:
        model = Invoice
        fields = '__all__'
    
    def get_total_tax(self, instance):
        return instance.calculate_total_tax()

    def get_total_amount_with_tax(self, instance):
        return instance.calculate_total_amount_with_tax()

    def get_total_amount_without_tax(self, instance):
        return instance.calculate_total_amount_without_tax()


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

class RepairLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairLog
        fields = "__all__"

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['name', 'quantity_to_order', 'last_order_date']


