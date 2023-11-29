from .models import ServiceRequest, Invoice, Part, ServiceTechnician, Customer
from rest_framework import generics
from .models import ServiceRequest, Invoice, Part, ServiceTechnician, Customer
from .serializers import (
    ServiceRequestSerializer, InvoiceSerializer, PartSerializer,
    ServiceTechnicianSerializer, CustomerSerializer
)


#def index(request):
    #return HttpResponse("Welcome in Computer service")


class ServiceRequestListAPIView(generics.ListCreateAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer

class ServiceRequestDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer

class InvoiceListAPIView(generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class InvoiceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class PartListAPIView(generics.ListCreateAPIView):
    queryset = Part.objects.all()
    serializer_class = PartSerializer

class PartDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Part.objects.all()
    serializer_class = PartSerializer

class ServiceTechnicianListAPIView(generics.ListCreateAPIView):
    queryset = ServiceTechnician.objects.all()
    serializer_class = ServiceTechnicianSerializer

class ServiceTechnicianDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceTechnician.objects.all()
    serializer_class = ServiceTechnicianSerializer

class CustomerListAPIView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CustomerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class ServiceRequestListCreateAPIView(generics.ListCreateAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer

class ServiceRequestDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer

class InvoiceListCreateAPIView(generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class InvoiceDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class PartListCreateAPIView(generics.ListCreateAPIView):
    queryset = Part.objects.all()
    serializer_class = PartSerializer

class PartDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Part.objects.all()
    serializer_class = PartSerializer

class ServiceTechnicianListCreateAPIView(generics.ListCreateAPIView):
    queryset = ServiceTechnician.objects.all()
    serializer_class = ServiceTechnicianSerializer

class ServiceTechnicianDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceTechnician.objects.all()
    serializer_class = ServiceTechnicianSerializer

class CustomerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CustomerDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

