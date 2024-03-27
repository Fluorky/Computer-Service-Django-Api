# computerserviceapp/serializers.py
from rest_framework import serializers
from .models import ServiceRequest, Invoice, Part, ServiceTechnician, Customer, RepairLog, Warehouse, Supplier, Address


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


class ServiceTechnicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceTechnician
        fields = '__all__'

    def create(self, validated_data):
        technician = ServiceTechnician.objects.create(
            email=validated_data['email'],
            username=validated_data['email'],
        )

        technician.set_password(validated_data['password'])
        technician.save()

        return technician

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('email', instance.email)
        instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.specialization = validated_data.get('specialization', instance.specialization)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.save()
        return instance


class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = '__all__'


class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
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


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
