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
        self.invoice = Invoice.objects.create(name='Invoice 21321', description='Computer repair services', requested_by=self.customer, owned_by=self.technician, total_amount=100.00)

    def test_models(self):
        self.assertEqual(str(self.customer), 'John Doe')
        self.assertEqual(str(self.technician), 'Tech Guy')
        self.assertEqual(str(self.service_request), 'Service')
        self.assertEqual(str(self.part), 'Hard Drive')
        self.assertEqual(str(self.invoice), 'Invoice 21321')

class ViewTests(TestCase):

    def setUp(self):
        # Create test data for views
        self.customer = Customer.objects.create(name='John', surname='Doe', email='john@example.com', phone_number='1234567890')
        self.technician = ServiceTechnician.objects.create(name='TechIT', surname='Guy', email='tech@example.com', phone_number='9876543210', specialization='Computer Repair')
        self.service_request = ServiceRequest.objects.create(name='Service', description='Fix my computer', requested_by=self.customer, owned_by=self.technician)
        self.part = Part.objects.create(name='Hard Drive', description='1TB HDD', quantity_in_stock=10)
        self.invoice = Invoice.objects.create(name='Invoice', description='Computer repair services', requested_by=self.customer, owned_by=self.technician, total_amount=100.00)

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'computerserviceapp/index.html')

    #Tests of service request views 

    def test_service_request_list_view(self):
        response = self.client.get(reverse('service_request_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'computerserviceapp/lists/service_request_list.html')

    def test_service_request_detail_view(self):
        response = self.client.get(reverse('service_request_detail', kwargs={'pk': self.service_request.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'computerserviceapp/details/service_request_detail.html')

    def test_service_request_create_view(self):
        response = self.client.get(reverse('service_request_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'computerserviceapp/forms/service_request_form.html')

    def test_service_request_update_view(self):
        response = self.client.get(reverse('service_request_edit', kwargs={'pk': self.service_request.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'computerserviceapp/forms/service_request_form.html')

    def test_service_request_delete_view(self):
        response = self.client.get(reverse('service_request_delete', kwargs={'pk': self.service_request.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'computerserviceapp/delete/service_request_confirm_delete.html')

    #Tests of invoice views 

    def test_invoice_list_view(self):
        response = self.client.get(reverse('invoice_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'computerserviceapp/lists/invoice_list.html')

    def test_invoice_detail_view(self):
        response = self.client.get(reverse('invoice_detail', kwargs={'pk': self.invoice.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'computerserviceapp/details/invoice_detail.html')

    def test_invoice_create_view(self):
        response = self.client.get(reverse('invoice_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'computerserviceapp/forms/invoice_form.html')

    def test_invoice_update_view(self):
        response = self.client.get(reverse('invoice_edit', kwargs={'pk': self.invoice.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'computerserviceapp/forms/invoice_form.html')

    def test_invoice_delete_view(self):
        response = self.client.get(reverse('invoice_delete', kwargs={'pk': self.invoice.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'computerserviceapp/delete/invoice_confirm_delete.html')

    #Tests of part views 

    def test_part_list_view(self):
        response = self.client.get(reverse('part_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'computerserviceapp/lists/part_list.html')

    def test_part_detail_view(self):
        response = self.client.get(reverse('part_detail', kwargs={'pk': self.part.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'computerserviceapp/details/part_detail.html')

    def test_part_create_view(self):
        response = self.client.get(reverse('part_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'computerserviceapp/forms/part_form.html')

    def test_part_update_view(self):
        response = self.client.get(reverse('part_edit', kwargs={'pk': self.part.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'computerserviceapp/forms/part_form.html')

    def test_part_delete_view(self):
        response = self.client.get(reverse('part_delete', kwargs={'pk': self.part.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'computerserviceapp/delete/part_confirm_delete.html')

    
    #Tests of service technician views 

    def test_service_technician_list_view(self):
        response = self.client.get(reverse('service_technician_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'computerserviceapp/lists/service_technician_list.html')

    def test_service_technician_detail_view(self):
        response = self.client.get(reverse('service_technician_detail', kwargs={'pk': self.technician.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'computerserviceapp/details/service_technician_detail.html')

    def test_service_technician_create_view(self):
        response = self.client.get(reverse('service_technician_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'computerserviceapp/forms/service_technician_form.html')

    def test_service_technician_update_view(self):
        response = self.client.get(reverse('service_technician_edit', kwargs={'pk': self.technician.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'computerserviceapp/forms/service_technician_form.html')

    def test_service_technician_delete_view(self):  
        response = self.client.get(reverse('service_technician_delete', kwargs={'pk': self.technician.pk }))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'computerserviceapp/delete/service_technician_confirm_delete.html')

     #Tests of customer views 

    def test_customer_list_view(self):
        response = self.client.get(reverse('customer_list'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'computerserviceapp/lists/customer_list.html')

    def test_customer_detail_view(self):
        response = self.client.get(reverse('customer_detail', kwargs={'pk':self.customer.pk}))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'computerserviceapp/details/customer_detail.html')

    def test_customer_create_view(self):
        response = self.client.get(reverse('customer_create'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'computerserviceapp/forms/customer_form.html')

    def test_customer_update_view(self):
        response = self.client.get(reverse('customer_edit', kwargs={'pk':self.customer.pk}))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'computerserviceapp/forms/customer_form.html')

    def test_customer_delete_view(self):
        response = self.client.get(reverse('customer_delete', kwargs={'pk':self.customer.pk}))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'computerserviceapp/delete/customer_confirm_delete.html')

    

    ##TO DO##
    # Add similar tests for other views


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
        form_data = {'name': 'Service', 'price': 10,'description': 'Fix my computer', 'requested_by': 1, 'owned_by': 1}
        form = ServiceRequestForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invoice_form_valid(self):
        form_data = {'name': 'Invoice 1','price': 21, 'description': 'Computer repair services', 'requested_by': 1, 'owned_by': 1, 'total_amount': 100.00, "payment_status":False}
        form = InvoiceForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_part_form_valid(self):
        form_data = {'name': 'Hard Drive','price': 100, 'description': '1TB HDD', 'quantity_in_stock': 10}
        form = PartForm(data=form_data)
        self.assertTrue(form.is_valid())

 
    ##TO DO##
    # Add similar tests for invalid form data, missing required fields, etc.
