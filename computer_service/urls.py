from django.urls import path
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('service-request/', views.service_request_list, name='service_request_list'),
    path('service-request/<int:pk>/', views.service_request_detail, name='service_request_detail'),
    path('service-request/new/', views.service_request_create, name='service_request_create'),
    path('service-request/<int:pk>/edit/', views.service_request_edit, name='service_request_edit'),
    path('service-request/<int:pk>/delete/', views.service_request_delete, name='service_request_delete'),

    #path('invoice/', views.invoice_list, name='invoice_list'),
    # Define similar URL patterns for Invoice Detail, Create, Update, Delete views...

    #path('part/', views.part_list, name='part_list'),
    # Define similar URL patterns for Part Detail, Create, Update, Delete views...

    #path('service-technician/', views.service_technician_list, name='service_technician_list'),
    # Define similar URL patterns for ServiceTechnician Detail, Create, Update, Delete views...

    #path('customer/', views.customer_list, name='customer_list'),
    # Define similar URL patterns for Customer Detail, Create, Update, Delete views...
]
