# computerserviceapp/tests.py

from django.test import TestCase
from django.urls import reverse
from .models import ServiceRequest, Invoice, Part, ServiceTechnician, Customer
from django.test import TestCase, Client
from django.urls import reverse
from .models import ServiceRequest, Invoice, Part, ServiceTechnician, Customer

class ModelTests(TestCase):
    def setUp(self):
        # Create test data for models
        self.customer = Customer.objects.create(name='John', surname='Doe', email='john@example.com', phone_number='1234567890')
        self.technician = ServiceTechnician.objects.create(name='Tech', surname='Guy', email='tech@example.com', phone_number='9876543210', specialization='Computer Repair')
        self.service_request = ServiceRequest.objects.create(name='Service', description='Fix my computer', requested_by=self.customer, owned_by=self.technician)
        self.part = Part.objects.create(name='Hard Drive', description='1TB HDD', quantity_in_stock=10)
        self.invoice = Invoice.objects.create(name='Invoice 21321', description='Computer repair services', requested_by=self.customer, owned_by=self.technician, total_amount=100.00)

    def test_models(self):
        self.assertEqual(str(self.customer), 'John Doe')
        self.assertEqual(str(self.technician), 'Tech Guy')
        self.assertEqual(str(self.service_request), 'Service')
        self.assertEqual(str(self.part), 'Hard Drive')
        self.assertEqual(str(self.invoice), 'Invoice 21321')


class ServiceRequestTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.customer = Customer.objects.create(name='John', surname='Doe', email='john@example.com', phone_number='1234567890')
        self.technician = ServiceTechnician.objects.create(name='TechIT', surname='Guy', email='tech@example.com', phone_number='9876543210', specialization='Computer Repair')
        self.service_request = ServiceRequest.objects.create(name='Service', description='Fix my computer', requested_by=self.customer, owned_by=self.technician)
        self.part = Part.objects.create(name='Hard Drive', description='1TB HDD', quantity_in_stock=10)
        self.invoice = Invoice.objects.create(name='Invoice', description='Computer repair services', requested_by=self.customer, owned_by=self.technician, total_amount=100.00)

    def test_service_request_list_view(self):
        response = self.client.get(reverse('service_request_list_api'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.service_request.name)
        self.assertContains(response, self.service_request.price)
        self.assertContains(response, self.service_request.description)
        # Add more assertions as needed

    def test_service_request_detail_view(self):
        response = self.client.get(reverse('service_request_detail_api', args=[self.service_request.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.service_request.name)
        self.assertContains(response, self.service_request.price)
        self.assertContains(response, self.service_request.description)
        # Add more assertions as needed

    def test_service_request_create_view(self):
        response = self.client.post(reverse('service_request_list_create_api'), {'name': 'New service Request', 'description': 'New Description', 'requested_by' :1 ,'owned_by':1})
        self.assertEqual(response.status_code, 201)  # Assuming a successful creation redirects to another page
        # Add more assertions as needed

    def test_service_request_update_view(self):
        response = self.client.get(reverse('service_request_detail_update_delete_api', args=[self.service_request.pk]))
        self.assertEqual(response.status_code, 200)

        response = self.client.put(
            reverse('service_request_detail_update_delete_api', args=[self.service_request.pk]),
            {'name': 'New service Request', 'price':100, 'description': 'New Description', 'requested_by' :1 ,'owned_by':1 },
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)  # Assuming a successful update redirects to another page

        self.service_request.refresh_from_db()
        self.assertEqual(self.service_request.name, 'New service Request')
        self.assertEqual(self.service_request.price, 100)
        self.assertEqual(self.service_request.description, 'New Description')
        #self.assertEqual(self.service_request.requested_by, 1)
        #self.assertEqual(self.service_request.owned_by, 1)
        
    def test_service_request_delete_view(self):
        response = self.client.delete(reverse('service_request_detail_update_delete_api', args=[self.service_request.pk]))
        self.assertEqual(response.status_code, 204)  # Assuming a successful deletion redirects to another page
        self.assertFalse(ServiceRequest.objects.filter(pk=self.service_request.pk).exists())
        # Add more assertions as needed
#TO DO##
# Similar tests can be created for other views (Invoice, Part, ServiceTechnician, Customer)

