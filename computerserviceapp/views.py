from django.shortcuts import get_object_or_404
from rest_framework import generics
from .models import ServiceRequest, Invoice, Part, ServiceTechnician, Customer, RepairLog, Warehouse,Comment,Address,Supplier
from .serializers import (
    ServiceRequestSerializer, InvoiceSerializer, PartSerializer,
    ServiceTechnicianSerializer, CustomerSerializer, RepairLogSerializer, WarehouseSerializer,CommentSerializer,AddressSerializer, SupplierSerializer
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

 
    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            instance = get_object_or_404(self.queryset, pk=kwargs['pk'])
            serializer = self.serializer_class(instance)
        else:
            queryset = self.queryset.all()
            serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

class CommentAPIView(CustomAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class SupplierAPIView(CustomAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class AddressAPIView(CustomAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


