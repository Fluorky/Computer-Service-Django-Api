# computerserviceapp/tests.py
# computerserviceapp/tests.py

from django.test import TestCase
from django.urls import reverse
from .models import ServiceRequest, Invoice, Part, ServiceTechnician, Customer
from .forms import ServiceRequestForm, InvoiceForm, PartForm, ServiceTechnicianForm, CustomerForm

class ModelTests(TestCase):
    def setUp(self):
        # Create test data for models
        self.customer = Customer.objects.create(name='John', surname='Doe', email='john@example.com', phone_number='1234567890')
        self.technician = ServiceTechnician.objects.create(name='Tech', surname='Guy', email='tech@example.com', phone_number='9876543210', specialization='Computer Repair')
        self.service_request = ServiceRequest.objects.create(name='Service', description='Fix my computer', requested_by=self.customer, owned_by=self.technician)
        self.part = Part.objects.create(name='Hard Drive', description='1TB HDD', quantity_in_stock=10)
        self.invoice = Invoice.objects.create(name='Invoice', description='Computer repair services', requested_by=self.customer, owned_by=self.technician, total_amount=100.00)

    def test_models(self):
        self.assertEqual(str(self.customer), 'John Doe')
        self.assertEqual(str(self.technician), 'Tech Guy')
        self.assertEqual(str(self.service_request), 'Service')
        self.assertEqual(str(self.part), 'Hard Drive')
        self.assertEqual(str(self.invoice), 'Invoice')

class ViewTests(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'computerserviceapp/index.html')

    def test_service_request_list_view(self):
        response = self.client.get(reverse('service_request_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'computerserviceapp/lists/service_request_list.html')

    ##TO DO##
    # Add similar tests for other forms




class FormTests(TestCase):
    def setUp(self):
        # Create test data for models
        self.customer = Customer.objects.create(name='John', surname='Doe', email='john@example.com', phone_number='1234567890')
        self.technician = ServiceTechnician.objects.create(name='Tech', surname='Guy', email='tech@example.com', phone_number='9876543210', specialization='Computer Repair')

    def test_service_technician_form_valid(self):
        form_data = {'name': 'Tech', 'surname': 'Guy', 'email': 'tech@example.com', 'phone_number': '9876543210', 'specialization': 'Computer Repair'}
        form = ServiceTechnicianForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_customer_form_valid(self):
        form_data = {'name': 'John', 'surname': 'Doe', 'email': 'john@example.com', 'phone_number': '1234567890', 'address_line1': '123 Main St', 'city': 'City', 'country': 'Country'}
        form = CustomerForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_service_request_form_valid(self):
        form_data = {'name': 'Service', 'price':10,'description': 'Fix my computer', 'requested_by': 1, 'owned_by': 1}
        form = ServiceRequestForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invoice_form_valid(self):
        form_data = {'name': 'Invoice 1','price':21, 'description': 'Computer repair services', 'requested_by': 1, 'owned_by': 1, 'total_amount': 100.00, "payment_status":False}
        form = InvoiceForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_part_form_valid(self):
        form_data = {'name': 'Hard Drive','price':100, 'description': '1TB HDD', 'quantity_in_stock': 10}
        form = PartForm(data=form_data)
        self.assertTrue(form.is_valid())

 
    ##TO DO##
    # Add similar tests for invalid form data, missing required fields, etc.
