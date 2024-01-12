from django.urls import path, include
from .views import (
    
    CreateUserView, LoginView, CreateUserView, LoginView,
    ServiceRequestAPIView, InvoiceAPIView,
    PartAPIView, ServiceTechnicianAPIView,
    CustomerAPIView, RepairLogAPIView,
    WarehouseAPIView
)
from rest_framework.authtoken.views import obtain_auth_token  

urlpatterns = [
    path('api/', include([
        path('service-requests/', ServiceRequestAPIView.as_view(), name='service_request_api'),
        path('invoices/', InvoiceAPIView.as_view(), name='invoice_api'),
        path('parts/', PartAPIView.as_view(), name='part_api'),
        path('service-technicians/', ServiceTechnicianAPIView.as_view(), name='service_technician_api'),
        path('customers/', CustomerAPIView.as_view(), name='customer_api'),
        path('repair-logs/', RepairLogAPIView.as_view(), name='repair_log_api'),
        path('warehouses/', WarehouseAPIView.as_view(), name='warehouse_api'),
        path('create-user/', CreateUserView.as_view(), name='create_user'),
        path('token/', obtain_auth_token, name='obtain-token'),
        path('login/', LoginView.as_view(), name='login'),
    ])),
]
