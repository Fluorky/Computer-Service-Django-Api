from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    CreateUserView, LoginView,
    ServiceRequestAPIView, InvoiceAPIView,
    PartAPIView, ServiceTechnicianAPIView,
    CustomerAPIView, RepairLogAPIView,
    WarehouseAPIView,  SupplierAPIView,  AddressAPIView
)
urlpatterns = [
    path('api/', include([
        path('service-requests/', ServiceRequestAPIView.as_view(), name='service_request_api'),
        path('service-requests/<int:pk>/', ServiceRequestAPIView.as_view(), name='service_request_detail_api'),
        path('invoices/', InvoiceAPIView.as_view(), name='invoice_api'),
        path('invoices/<int:pk>/', InvoiceAPIView.as_view(), name='invoice_detail_api'),
        path('parts/', PartAPIView.as_view(), name='part_api'),
        path('parts/<int:pk>/', PartAPIView.as_view(), name='part_detail_api'),
        path('service-technicians/', ServiceTechnicianAPIView.as_view(), name='service_technician_api'),
        path('service-technicians/<int:pk>/', ServiceTechnicianAPIView.as_view(), name='service_technician_detail_api'),
        path('customers/', CustomerAPIView.as_view(), name='customer_api'),
        path('customers/<int:pk>/', CustomerAPIView.as_view(), name='customer_detail_api'),
        path('repair-logs/', RepairLogAPIView.as_view(), name='repair_log_api'),
        path('repair-logs/<int:pk>/', RepairLogAPIView.as_view(), name='repair_log_detail_api'),
        path('warehouses/', WarehouseAPIView.as_view(), name='warehouse_api'),
        path('warehouses/<int:pk>/', WarehouseAPIView.as_view(), name='warehouse_detail_api'),
        path('address/',AddressAPIView.as_view(),name='address_api'),
        path('address/<int:pk>/',AddressAPIView.as_view(),name='address_detail_api'),
        path('supplier/',SupplierAPIView.as_view(),name='supplier_api'),
        path('supplier/<int:pk>/',SupplierAPIView.as_view(),name='supplier_detail_api'),
        path('create-user/', CreateUserView.as_view(), name='create_user'),
        path('token/', obtain_auth_token, name='obtain-token'),
        path('login/', LoginView.as_view(), name='login'),
    ])),
]
