from django.urls import path
from . import views
from .views import IndexView,ServiceRequestListView, ServiceRequestDetailView, ServiceRequestCreateView, ServiceRequestUpdateView, ServiceRequestDeleteView
from django.views.generic.base import RedirectView

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
