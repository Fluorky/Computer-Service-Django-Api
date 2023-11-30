from django.urls import path
from .views import (
    ServiceRequestListAPIView, ServiceRequestDetailAPIView,
    InvoiceListAPIView, InvoiceDetailAPIView,
    PartListAPIView, PartDetailAPIView,
    ServiceTechnicianListAPIView, ServiceTechnicianDetailAPIView,
    CustomerListAPIView, CustomerDetailAPIView,
    ServiceRequestListCreateAPIView, ServiceRequestDetailUpdateDeleteAPIView,
    InvoiceListCreateAPIView, InvoiceDetailUpdateDeleteAPIView,
    PartListCreateAPIView, PartDetailUpdateDeleteAPIView,
    ServiceTechnicianListCreateAPIView, ServiceTechnicianDetailUpdateDeleteAPIView,
    CustomerListCreateAPIView, CustomerDetailUpdateDeleteAPIView
)

urlpatterns = [
    path('api/service-requests/', ServiceRequestListAPIView.as_view(), name='service_request_list_api'),
    path('api/service-requests/<int:pk>/', ServiceRequestDetailAPIView.as_view(), name='service_request_detail_api'),
    path('api/service-requests/', ServiceRequestListCreateAPIView.as_view(), name='service_request_list_create_api'),
    path('api/service-requests/<int:pk>/', ServiceRequestDetailUpdateDeleteAPIView.as_view(), name='service_request_detail_update_delete_api'),

    path('api/invoices/', InvoiceListAPIView.as_view(), name='invoice_list_api'),
    path('api/invoices/<int:pk>/', InvoiceDetailAPIView.as_view(), name='invoice_detail_api'),
    path('api/invoices/', InvoiceListCreateAPIView.as_view(), name='invoice_list_create_api'),
    path('api/invoices/<int:pk>/', InvoiceDetailUpdateDeleteAPIView.as_view(), name='invoice_detail_update_delete_api'),

    path('api/parts/', PartListAPIView.as_view(), name='part_list_api'),
    path('api/parts/<int:pk>/', PartDetailAPIView.as_view(), name='part_detail_api'),
    path('api/parts/', PartListCreateAPIView.as_view(), name='part_list_create_api'),
    path('api/parts/<int:pk>/', PartDetailUpdateDeleteAPIView.as_view(), name='part_detail_update_delete_api'),

    path('api/service-technicians/', ServiceTechnicianListAPIView.as_view(), name='service_technician_list_api'),
    path('api/service-technicians/<int:pk>/', ServiceTechnicianDetailAPIView.as_view(), name='service_technician_detail_api'),
    path('api/service-technicians/', ServiceTechnicianListCreateAPIView.as_view(), name='service_technician_list_create_api'),
    path('api/service-technicians/<int:pk>/', ServiceTechnicianDetailUpdateDeleteAPIView.as_view(), name='service_technician_detail_update_delete_api'),

    path('api/customers/', CustomerListAPIView.as_view(), name='customer_list_api'),
    path('api/customers/<int:pk>/', CustomerDetailAPIView.as_view(), name='customer_detail_api'),
    path('api/customers/', CustomerListCreateAPIView.as_view(), name='customer_list_create_api'),
    path('api/customers/<int:pk>/', CustomerDetailUpdateDeleteAPIView.as_view(), name='customer_detail_update_delete_api'),
]

