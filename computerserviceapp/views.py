from rest_framework import generics
from .models import ServiceRequest, Invoice, Part, ServiceTechnician, Customer, RepairLog, Warehouse
from .serializers import (
    ServiceRequestSerializer, InvoiceSerializer, PartSerializer,
    ServiceTechnicianSerializer, CustomerSerializer, RepairLogSerializer, WarehouseSerializer
)


class ServiceRequestListAPIView(generics.ListCreateAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer

class ServiceRequestDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer

class ServiceRequestListCreateAPIView(generics.ListCreateAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer

class ServiceRequestDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer

class InvoiceListAPIView(generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class InvoiceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class InvoiceListCreateAPIView(generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class InvoiceDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class PartListAPIView(generics.ListCreateAPIView):
    queryset = Part.objects.all()
    serializer_class = PartSerializer

class PartDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Part.objects.all()
    serializer_class = PartSerializer

class PartListCreateAPIView(generics.ListCreateAPIView):
    queryset = Part.objects.all()
    serializer_class = PartSerializer

class PartDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Part.objects.all()
    serializer_class = PartSerializer

class ServiceTechnicianListAPIView(generics.ListCreateAPIView):
    queryset = ServiceTechnician.objects.all()
    serializer_class = ServiceTechnicianSerializer

class ServiceTechnicianDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceTechnician.objects.all()
    serializer_class = ServiceTechnicianSerializer

class ServiceTechnicianListCreateAPIView(generics.ListCreateAPIView):
    queryset = ServiceTechnician.objects.all()
    serializer_class = ServiceTechnicianSerializer

class ServiceTechnicianDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceTechnician.objects.all()
    serializer_class = ServiceTechnicianSerializer

class CustomerListAPIView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CustomerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CustomerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CustomerDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class RepairLogListAPIView(generics.ListCreateAPIView):
    queryset = RepairLog.objects.all()
    serializer_class = RepairLogSerializer

class RepairLogDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RepairLog.objects.all()
    serializer_class = RepairLogSerializer

class RepairLogListCreateAPIView(generics.ListCreateAPIView):
    queryset = RepairLog.objects.all()
    serializer_class = RepairLogSerializer

class RepairLogDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RepairLog.objects.all()
    serializer_class = RepairLogSerializer

class WarehouseListAPIView(generics.ListCreateAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

class WarehouseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

class WarehouseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

class WarehouseDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer



