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


"""
class LoginView(APIView):
    permission_classes= [AllowAny, ]
    def post(self, request, *args, **kwargs):
        username= request.data.get('username')
        password = request.data.get('password')
        #print(f"Email: {username}, Password: {password}")  # Debugging line
        #cf = ServiceTechnician.objects.filter(username=username).first()
        #print(cf)
        #print(cf.check_password(password))

        user = authenticate(request, username=username, password=password)
        print(user)
        if user:
        #if cf and cf.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
"""

"""
class CreateUserView(APIView):
    permission_classes = [AllowAny, ]
    def post(self, request, *args, **kwargs):
        # Extract username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user with the given username already exists
        if ServiceTechnician.objects.filter(username=username).exists():
            return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)

        # Create and save the new user
        new_user = ServiceTechnician.objects.create(
            username=username,
            password=make_password(password)  # Hash the password
        )
        new_user.save()

        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
"""
"""
#class CreateServiceTechnicianView(APIView):
class CreateUserView(APIView):
    permission_classes = [AllowAny, ]
    def post(self, request, *args, **kwargs):
        # Extract username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')
        user_ptr_id = request.data.get('user_ptr_id')


        if not username or not password :
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user with the given username already exists
        if ServiceTechnician.objects.filter(username=username).exists():
            return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)

        # Create and save the new user
        new_user = ServiceTechnician.objects.create(
            username=username,
            password=make_password(password), # Hash the password
            user_ptr_id=user_ptr_id
            
        )
        new_user.save()

        return Response({'message': 'Service technician created successfully'}, status=status.HTTP_201_CREATED)
"""







"""
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
    #permission_classes = [AllowAny, ]
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



"""

class CustomAPIView(generics.GenericAPIView):
    queryset = None
    serializer_class = None
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, pk):
        try:
            return self.queryset.objects.get(pk=pk)
        except self.queryset.model.DoesNotExist:
            raise Response({'error': f'{self.queryset.model.__name__} not found'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            instance = self.get_object(kwargs['pk'])
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
        instance = self.get_object(kwargs['pk'])
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object(kwargs['pk'])
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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