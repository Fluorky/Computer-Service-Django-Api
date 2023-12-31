# computerserviceapp/tests.py

import json
from django.test import TestCase, Client
from django.urls import reverse
from .models import ServiceRequest, Invoice, Part, ServiceTechnician, Customer
from django.contrib.auth.hashers import make_password



class BaseTestCase(TestCase):
    def setUp(self):
        # Create test data for models
        hashed_password = make_password('Test123.')
        self.customer = Customer.objects.create(name='John', surname='Doe', email='john@example.com', phone_number='1234567890')
        self.technician = ServiceTechnician.objects.create(first_name='TechIT', last_name='Guy', username='Tech', email='tech@example.com', phone_number='9876543210', specialization='Computer Repair',is_superuser=True,is_staff=True,is_active=True, password=hashed_password)
        self.service_request = ServiceRequest.objects.create(name='Service', description='Fix my computer', requested_by=self.customer, owned_by=self.technician)
        self.part = Part.objects.create(name='Hard Drive', description='1TB HDD', quantity_in_stock=10)
        self.invoice = Invoice.objects.create(name='Invoice', total_amount=100.00)
        self.invoice.parts.set([self.part])
        self.invoice.service_requests.set([self.service_request])
   

    def test_token_generation(self):
        self.client = Client()


        url = reverse('obtain-token')
       
        data = {
            'username': 'tech@example.com',
            'password': 'Test123.'
        }
   
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)
        token=content['token']

        headers = {
            'Authorization': f'Token {token}',
        }

        response = self.client.get(reverse('service_technician_list_api'), headers=headers)
        self.assertEqual(response.status_code,200)
        #self.assertEqual(response.content, "XD")


class ModelTests(BaseTestCase):
    def test_models(self):
        self.assertEqual(str(self.customer), 'John Doe')
        self.assertEqual(str(self.technician), 'Tech Computer Repair')
        self.assertEqual(str(self.technician.email), 'tech@example.com')
        self.assertEqual(str(self.technician.username), 'Tech')
        self.assertEqual(str(self.technician.is_active), 'True')
  
    


class ServiceRequestTests(BaseTestCase):
        



    def test_service_request_list_view(self):
        
        response = self.client.get(reverse('service_request_list_api'),headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.service_request.name)
        self.assertContains(response, self.service_request.price)
        self.assertContains(response, self.service_request.description)

    

    def test_models(self):

        service_request = ServiceRequest.objects.get(pk=1)   
        self.assertEqual(service_request.state,"new")
        service_request.submit_request()  # Move to 'open' state
        self.assertEqual(service_request.state,"open")
        service_request.start_work()  # Move to 'pending' state
        self.assertEqual(service_request.state,"pending")
        service_request.mark_in_progress()  # Move to 'work_in_progress' state
        self.assertEqual(service_request.state,"work_in_progress")

      
        

    def test_service_request_detail_view(self):
        response = self.client.get(reverse('service_request_detail_api', args=[self.service_request.pk]),self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.service_request.name)
        self.assertContains(response, self.service_request.price)
        self.assertContains(response, self.service_request.description)
     
  


    def test_service_request_create_view(self):
        response = self.client.post(reverse('service_request_list_create_api'),{'name': 'New service Request', 'description': 'New Description', 'requested_by' :1 ,'owned_by':1},headers=self.headers)
        self.assertEqual(response.status_code, 201)  # Assuming a successful creation redirects to another page
       

    def test_service_request_update_view(self):
        response = self.client.get(reverse('service_request_detail_update_delete_api', args=[self.service_request.pk]),headers=self.headers)
        self.assertEqual(response.status_code, 200)

        response = self.client.put(
            reverse('service_request_detail_update_delete_api', args=[self.service_request.pk]),
            {'name': 'New service Request', 'price':100, 'description': 'New Description', 'requested_by' :1 ,'owned_by':1 },
            content_type='application/json',headers=self.headers
        )

        self.assertEqual(response.status_code, 200)  # Assuming a successful update redirects to another page

        self.service_request.refresh_from_db()
        self.assertEqual(self.service_request.name, 'New service Request')
        self.assertEqual(self.service_request.price, 100)
        self.assertEqual(self.service_request.description, 'New Description')
        self.assertEqual(self.service_request.requested_by, self.customer)
        self.assertEqual(self.service_request.owned_by, self.technician)
        
    def test_service_request_delete_view(self):
        response = self.client.delete(reverse('service_request_detail_update_delete_api', args=[self.service_request.pk]),headers=self.headers)
        self.assertEqual(response.status_code, 204)  # Assuming a successful deletion redirects to another page
        self.assertFalse(ServiceRequest.objects.filter(pk=self.service_request.pk).exists())
        
class InvoiceTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.customer = Customer.objects.create(name='John', surname='Doe', email='john@example.com', phone_number='1234567890')
        self.technician = ServiceTechnician.objects.create(first_name='TechIT', last_name='Guy', username="Tech", email='tech@example.com', phone_number='9876543210', specialization='Computer Repair', password="Test123.")
        self.service_request = ServiceRequest.objects.create(name='Service', description='Fix my computer', requested_by=self.customer, owned_by=self.technician)
        self.part = Part.objects.create(name='Hard Drive', description='1TB HDD', quantity_in_stock=10)
        self.invoice = Invoice.objects.create(name='Invoice', total_amount=100.00)
        self.invoice.parts.set([self.part])
        self.invoice.service_requests.set([self.service_request])
        #self.invoice = Invoice.objects.create(name='Invoice', description='Computer repair services', requested_by=self.customer, owned_by=self.technician, total_amount=100.00, part=self.part, service_request=self.service_request)
       
    def test_invoice_list_view(self):
        response = self.client.get(reverse('invoice_list_api'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.invoice.name)
        self.assertContains(response, self.invoice.price)
        self.assertContains(response, self.invoice.description)
        self.assertContains(response, self.invoice.total_amount)
      

    def test_invoice_detail_view(self):
        response = self.client.get(reverse('invoice_detail_api', args=[self.invoice.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.invoice.name)
        self.assertContains(response, self.invoice.price)
        self.assertContains(response, self.invoice.description)
        self.assertContains(response, self.invoice.total_amount)


    def test_invoice_create_view(self):
        response = self.client.post(reverse('invoice_list_create_api'), {'name': 'Invoice 3241', 'description': 'Fix screen errors', 'requested_by' :1 ,'owned_by':1,'total_amount':100.00, 'part':1, 'service_request':1})
        self.assertEqual(response.status_code, 201)  # Assuming a successful creation redirects to another page
       

    def test_invoice_update_view(self):
        response = self.client.get(reverse('invoice_detail_update_delete_api', args=[self.invoice.pk]))
        self.assertEqual(response.status_code, 200)

        response = self.client.put(
            reverse('invoice_detail_update_delete_api', args=[self.invoice.pk]),
            {'name': 'Invoice 123423', 'description': 'Fix laptop drive', 'requested_by' :1 ,'owned_by':1,'total_amount':200.00,'part':1, 'service_request':1},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)  # Assuming a successful update redirects to another page

        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.name, 'Invoice 123423')
        self.assertEqual(self.invoice.total_amount, 200.00)
        self.assertEqual(self.invoice.description, 'Fix laptop drive')
        self.assertEqual(self.invoice.requested_by, self.customer)
        self.assertEqual(self.invoice.owned_by, self.technician)
        self.assertEqual(self.invoice.part, self.part)
        self.assertEqual(self.invoice.service_request, self.service_request)

        
    def test_invoice_delete_view(self):
        response = self.client.delete(reverse('invoice_detail_update_delete_api', args=[self.invoice.pk]))
        self.assertEqual(response.status_code, 204)  # Assuming a successful deletion redirects to another page
        self.assertFalse(Invoice.objects.filter(pk=self.invoice.pk).exists())


    def test_part_detail_view(self):
        response = self.client.get(reverse('part_detail_api', args=[self.part.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.part.name)
        self.assertContains(response, self.part.price)
        self.assertContains(response, self.part.description)
        self.assertContains(response, self.part.quantity_in_stock)


    def test_part_create_view(self):
        response = self.client.post(reverse('part_list_create_api'), {'name':'Hard Drive', 'description':'1TB HDD', 'quantity_in_stock':10})
        self.assertEqual(response.status_code, 201)  # Assuming a successful creation redirects to another page
       

    def test_part_update_view(self):
        response = self.client.get(reverse('part_detail_update_delete_api', args=[self.part.pk]))
        self.assertEqual(response.status_code, 200)

        response = self.client.put(
            reverse('part_detail_update_delete_api', args=[self.part.pk]),
            {'name':'Hard Drive', 'description':'1TB SSD', 'quantity_in_stock':10},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)  # Assuming a successful update redirects to another page

        self.part.refresh_from_db()
        self.assertEqual(self.part.name, 'Hard Drive')
        self.assertEqual(self.part.quantity_in_stock, 10)
        self.assertEqual(self.part.price, 0.00)
        self.assertEqual(self.part.description, '1TB SSD')
        
    def test_part_delete_view(self):
        response = self.client.delete(reverse('part_detail_update_delete_api', args=[self.part.pk]))
        self.assertEqual(response.status_code, 204)  # Assuming a successful deletion redirects to another page
        self.assertFalse(Part.objects.filter(pk=self.part.pk).exists())

class ServiceTechnicianTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.customer = Customer.objects.create(name='John', surname='Doe', email='john@example.com', phone_number='1234567890')
        self.technician = ServiceTechnician.objects.create(first_name='TechIT', last_name='Guy', username="Tech", email='tech@example.com', phone_number='9876543210', specialization='Computer Repair', password="Test123.")
        self.service_request = ServiceRequest.objects.create(name='Service', description='Fix my computer', requested_by=self.customer, owned_by=self.technician)
        self.part = Part.objects.create(name='Hard Drive', description='1TB HDD', quantity_in_stock=10)
        self.invoice = Invoice.objects.create(name='Invoice', total_amount=100.00)
        self.invoice.parts.set([self.part])
        self.invoice.service_requests.set([self.service_request])
    
        
        #self.invoice = Invoice.objects.create(name='Invoice', total_amount=100.00, parts=self.part, service_requests=self.service_request)#description='Computer repair services', requested_by=self.customer, owned_by=self.technician)
    def test_service_technician_list_view(self):
        response = self.client.get(reverse('service_technician_list_api'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.technician.first_name)
        self.assertContains(response, self.technician.last_name)
        self.assertContains(response, self.technician.email)
        self.assertContains(response, self.technician.phone_number)
        self.assertContains(response, self.technician.specialization)
        

    def test_service_technician_detail_view(self):
        response = self.client.get(reverse('service_technician_detail_api', args=[self.technician.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.technician.first_name)
        self.assertContains(response, self.technician.last_name)
        self.assertContains(response, self.technician.email)
        self.assertContains(response, self.technician.phone_number)
        self.assertContains(response, self.technician.specialization)
  
       

    def test_service_technician_create_view(self):
        response = self.client.post(reverse('service_technician_list_create_api'), {'first_name':'Rajesh', 'last_name':'Rax', 'email':'rajeshrax@example.com', 'phone_number':'9874343210', 'specialization':'IT support'})
        self.assertEqual(response.status_code, 201)  # Assuming a successful creation redirects to another page
       

    def test_service_technician_update_view(self):
        response = self.client.get(reverse('service_technician_detail_update_delete_api', args=[self.technician.pk]))
        self.assertEqual(response.status_code, 200)

        response = self.client.put(
            reverse('service_technician_detail_update_delete_api', args=[self.technician.pk]),
            {'first_name':'Rajesh', 'last_name':'Hrejt', 'email':'rajeshhrejt@example.com', 'phone_number':'9874343210', 'specialization':'IT programmer'},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)  # Assuming a successful update redirects to another page

        self.technician.refresh_from_db()
        self.assertEqual(self.technician.first_name, 'Rajesh')
        self.assertEqual(self.technician.last_name, 'Hrejt')
        self.assertEqual(self.technician.email, 'rajeshhrejt@example.com')
        self.assertEqual(self.technician.phone_number, '9874343210')
        self.assertEqual(self.technician.specialization, 'IT programmer')
        
    def test_service_technician_delete_view(self):
        response = self.client.delete(reverse('service_technician_detail_update_delete_api', args=[self.technician.pk]))
        self.assertEqual(response.status_code, 204)  # Assuming a successful deletion redirects to another page
        self.assertFalse(ServiceTechnician.objects.filter(pk=self.technician.pk).exists())



class CustomerTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.customer = Customer.objects.create(name='John', surname='Doe', email='john@example.com', phone_number='1234567890')
        self.technician = ServiceTechnician.objects.create(first_name='TechIT', last_name='Guy', username="Tech", email='tech@example.com', phone_number='9876543210', specialization='Computer Repair', password="Test123.")
        self.service_request = ServiceRequest.objects.create(name='Service', description='Fix my computer', requested_by=self.customer, owned_by=self.technician)
        self.part = Part.objects.create(name='Hard Drive', description='1TB HDD', quantity_in_stock=10)
        self.invoice = Invoice.objects.create(name='Invoice', total_amount=100.00)
        self.invoice.parts.set([self.part])
        self.invoice.service_requests.set([self.service_request])
        #self.invoice = Invoice.objects.create(name='Invoice', total_amount=100.00, parts=self.part, service_requests=self.service_request)#description='Computer repair services', requested_by=self.customer, owned_by=self.technician)
        #self.invoice = Invoice.objects.create(name='Invoice', total_amount=100.00, parts=self.part, service_requests=self.service_request)#description='Computer repair services', requested_by=self.customer, owned_by=self.technician)
    
    def test_customer_list_view(self):
        response = self.client.get(reverse('customer_list_api'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.customer.name)
        self.assertContains(response, self.customer.surname)
        self.assertContains(response, self.customer.email)
        self.assertContains(response, self.customer.phone_number)

        

    def test_customer_detail_view(self):
        response = self.client.get(reverse('customer_detail_api', args=[self.customer.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.customer.name)
        self.assertContains(response, self.customer.surname)
        self.assertContains(response, self.customer.email)
        self.assertContains(response, self.customer.phone_number)
        
       

    def test_customer_create_view(self):
        response = self.client.post(reverse('customer_list_create_api'), {'name':'Rajesh', 'surname':'Rax', 'email':'rajeshrax@example.com', 'phone_number':'9874343210', 'specialization':'IT support'})
        self.assertEqual(response.status_code, 201)  # Assuming a successful creation redirects to another page
       

    def test_customer_update_view(self):
        response = self.client.get(reverse('customer_detail_update_delete_api', args=[self.customer.pk]))
        self.assertEqual(response.status_code, 200)

        response = self.client.put(
            reverse('customer_detail_update_delete_api', args=[self.customer.pk]),
            {'name':'Pajet', 'surname':'Hrejt', 'email':'pajethrejt@example.com', 'phone_number':'9874343210', 'specialization':'IT programmer'},
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)  # Assuming a successful update redirects to another page

        self.customer.refresh_from_db()
        self.assertEqual(self.customer.name, 'Pajet')
        self.assertEqual(self.customer.surname, 'Hrejt')
        self.assertEqual(self.customer.email, 'pajethrejt@example.com')
        self.assertEqual(self.customer.phone_number, '9874343210')

        
    def test_customer_delete_view(self):
        response = self.client.delete(reverse('customer_detail_update_delete_api', args=[self.customer.pk]))
        self.assertEqual(response.status_code, 204)  # Assuming a successful deletion redirects to another page
        self.assertFalse(Customer.objects.filter(pk=self.customer.pk).exists())


