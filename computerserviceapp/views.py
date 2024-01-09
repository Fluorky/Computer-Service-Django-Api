from rest_framework import generics
from .models import ServiceRequest, Invoice, Part, ServiceTechnician, Customer, RepairLog, Warehouse
from .serializers import (
    ServiceRequestSerializer, InvoiceSerializer, PartSerializer,
    ServiceTechnicianSerializer, CustomerSerializer, RepairLogSerializer, WarehouseSerializer
)
from rest_framework.permissions import IsAuthenticated  # Import the IsAuthenticated permission
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate


class LoginView(APIView):
    #permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user:

            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)

            return Response({'token': token.key, 'user': str(user)}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class CreateUserView(APIView):
    #permission_classes = [AllowAny, ]
    def post(self, request, *args, **kwargs):
        # Extract username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password or not email:
            return Response({'error': 'Username email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user with the given username already exists
        if ServiceTechnician.objects.filter(username=username).exists():
            return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)

        if ServiceTechnician.objects.filter(email=email).exists():
            return Response({'error': 'Email already taken'}, status=status.HTTP_400_BAD_REQUEST)
        # Create and save the new user
        new_user = ServiceTechnician.objects.create(
            username=username,
            email=email,
            password=make_password(password)  # Hash the password
        )
        new_user.save()

        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)


class CustomAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = None
    serializer_class = None
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self):
        if 'pk' in self.kwargs:
            return generics.get_object_or_404(self.queryset, pk=self.kwargs['pk'])
        return self.queryset.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ServiceRequestAPIView(CustomAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer

class InvoiceAPIView(CustomAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class PartAPIView(CustomAPIView):
    queryset = Part.objects.all()
    serializer_class = PartSerializer

class ServiceTechnicianAPIView(CustomAPIView):
    queryset = ServiceTechnician.objects.all()
    serializer_class = ServiceTechnicianSerializer

class CustomerAPIView(CustomAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class RepairLogAPIView(CustomAPIView):
    queryset = RepairLog.objects.all()
    serializer_class = RepairLogSerializer

class WarehouseAPIView(CustomAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
