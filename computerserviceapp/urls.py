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

"""
urlpatterns = [
    #path('', views.index, name='index'),
    path('', IndexView.as_view() ,name='index'),
    path('service-request/', ServiceRequestListView.as_view(), name='service_request_list'),
    path('service-request/<int:pk>/', ServiceRequestDetailView.as_view(), name='service_request_detail'),
    path('service-request/new/', ServiceRequestCreateView.as_view(), name='service_request_create'),
    path('service-request/<int:pk>/edit/', ServiceRequestUpdateView.as_view(), name='service_request_edit'),
    path('service-request/<int:pk>/delete/', ServiceRequestDeleteView.as_view(), name='service_request_delete'),

    #path('service-request/', views.service_request_list, name='service_request_list'),
    #path('service-request/<int:pk>/', views.service_request_detail, name='service_request_detail'),
    #path('service-request/new/', views.service_request_create, name='service_request_create'),
    #path('service-request/<int:pk>/edit/', views.service_request_edit, name='service_request_edit'),
    #path('service-request/<int:pk>/delete/', views.service_request_delete, name='service_request_delete'),
    

    path('invoice/', views.invoice_list, name='invoice_list'),
    path('invoice/<int:pk>/', views.invoice_detail, name='invoice_detail'),
    path('invoice/new/', views.invoice_create, name='invoice_create'),
    path('invoice/<int:pk>/edit/', views.invoice_edit, name='invoice_edit'),
    path('invoice/<int:pk>/delete/', views.invoice_delete, name='invoice_delete'),

    path('part/', views.part_list, name='part_list'),
    path('part/<int:pk>/', views.part_detail, name='part_detail'),
    path('part/new/', views.part_create, name='part_create'),
    path('part/<int:pk>/edit/', views.part_edit, name='part_edit'),
    path('part/<int:pk>/delete/', views.part_delete, name='part_delete'),

    path('service-technician/', views.service_technician_list, name='service_technician_list'),
    path('service-technician/<int:pk>/', views.service_technician_detail, name='service_technician_detail'),
    path('service-technician/new/', views.service_technician_create, name='service_technician_create'),
    path('service-technician/<int:pk>/edit/', views.service_technician_edit, name='service_technician_edit'),
    path('service-technician/<int:pk>/delete/', views.service_technician_delete, name='service_technician_delete'),

    path('customer/', views.customer_list, name='customer_list'),
    path('customer/<int:pk>/', views.customer_detail, name='customer_detail'),
    path('customer/new/', views.customer_create, name='customer_create'),
    path('customer/<int:pk>/edit/', views.customer_edit, name='customer_edit'),
    path('customer/<int:pk>/delete/', views.customer_delete, name='customer_delete')

]
"""