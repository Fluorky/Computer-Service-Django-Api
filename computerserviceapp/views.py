from rest_framework import generics
from .models import ServiceRequest, Invoice, Part, ServiceTechnician, Customer, RepairLog, Warehouse
from .serializers import (
    ServiceRequestSerializer, InvoiceSerializer, PartSerializer,
    ServiceTechnicianSerializer, CustomerSerializer, RepairLogSerializer, WarehouseSerializer
)
from rest_framework.permissions import IsAuthenticated  # Import the IsAuthenticated permission
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class CreateUserView(APIView):
    def post(self, request, *args, **kwargs):
        # Extract username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user with the given username already exists
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)

        # Create and save the new user
        new_user = User.objects.create(
            username=username,
            password=make_password(password)  # Hash the password
        )
        new_user.save()

        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)


class ServiceRequestListAPIView(generics.ListCreateAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    permission_classes = [IsAuthenticated]  
    authentication_classes = [TokenAuthentication]


class ServiceRequestDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    permission_classes = [IsAuthenticated] 
    authentication_classes = [TokenAuthentication]


class ServiceRequestListCreateAPIView(generics.ListCreateAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    permission_classes = [IsAuthenticated] 
    authentication_classes = [TokenAuthentication]


class ServiceRequestDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    permission_classes = [IsAuthenticated] 
    authentication_classes = [TokenAuthentication]

class InvoiceListAPIView(generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated] 
    authentication_classes = [TokenAuthentication]

class InvoiceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated] 
    authentication_classes = [TokenAuthentication]

class InvoiceListCreateAPIView(generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated] 
    authentication_classes = [TokenAuthentication]


class InvoiceDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated] 
    authentication_classes = [TokenAuthentication]

class PartListAPIView(generics.ListCreateAPIView):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    permission_classes = [IsAuthenticated] 
    authentication_classes = [TokenAuthentication]

class PartDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    permission_classes = [IsAuthenticated] 
    authentication_classes = [TokenAuthentication]

class PartListCreateAPIView(generics.ListCreateAPIView):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    permission_classes = [IsAuthenticated] 
    authentication_classes = [TokenAuthentication]

class PartDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    permission_classes = [IsAuthenticated] 
    authentication_classes = [TokenAuthentication]

class ServiceTechnicianListAPIView(generics.ListCreateAPIView):
    queryset = ServiceTechnician.objects.all()
    serializer_class = ServiceTechnicianSerializer
    permission_classes = [IsAuthenticated] 
    authentication_classes = [TokenAuthentication]

class ServiceTechnicianDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceTechnician.objects.all()
    serializer_class = ServiceTechnicianSerializer
    permission_classes = [IsAuthenticated] 
    authentication_classes = [TokenAuthentication]

class ServiceTechnicianListCreateAPIView(generics.ListCreateAPIView):
    queryset = ServiceTechnician.objects.all()
    serializer_class = ServiceTechnicianSerializer
    permission_classes = [IsAuthenticated] 
    authentication_classes = [TokenAuthentication]

class ServiceTechnicianDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceTechnician.objects.all()
    serializer_class = ServiceTechnicianSerializer
    permission_classes = [IsAuthenticated] 
    authentication_classes = [TokenAuthentication]

class CustomerListAPIView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated] 
    authentication_classes = [TokenAuthentication]

class CustomerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated] 
    authentication_classes = [TokenAuthentication]

class CustomerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated] 
    authentication_classes = [TokenAuthentication]

class CustomerDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated] 
    authentication_classes = [TokenAuthentication]

class RepairLogListAPIView(generics.ListCreateAPIView):
    queryset = RepairLog.objects.all()
    serializer_class = RepairLogSerializer
    permission_classes = [IsAuthenticated] 
    authentication_classes = [TokenAuthentication]

class RepairLogDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RepairLog.objects.all()
    serializer_class = RepairLogSerializer
    permission_classes = [IsAuthenticated] 
    authentication_classes = [TokenAuthentication]

class RepairLogListCreateAPIView(generics.ListCreateAPIView):
    queryset = RepairLog.objects.all()
    serializer_class = RepairLogSerializer
    permission_classes = [IsAuthenticated] 
    authentication_classes = [TokenAuthentication]

class RepairLogDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RepairLog.objects.all()
    serializer_class = RepairLogSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication] 

class WarehouseListAPIView(generics.ListCreateAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication] 

class WarehouseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer    
    permission_classes = [IsAuthenticated] 
    authentication_classes = [TokenAuthentication]

class WarehouseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated] 
    authentication_classes = [TokenAuthentication]

class WarehouseDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated] 
    authentication_classes = [TokenAuthentication]



