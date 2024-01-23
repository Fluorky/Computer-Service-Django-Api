# computerserviceapp/tests.py
import json
from django.test import TestCase, Client
from django.urls import reverse
from .models import ServiceRequest, Invoice, Part, ServiceTechnician, Customer,Address,Comment,RepairLog,Supplier,Warehouse
from django.contrib.auth.hashers import make_password

class BaseTestCase(TestCase):
    
    def setUp(self):
        # Create test data for models
        self.hashed_password = make_password(password='Test123.')
        self.customer = Customer.objects.create(
            name='John', 
            surname='Doe', 
            email='john@example.com', 
            phone_number='1234567890'
        )
        self.technician = ServiceTechnician.objects.create(
            first_name='TechIT', 
            last_name='Guy', 
            username='Tech', 
            email='tech@example.com', 
            phone_number='9876543210', 
            specialization='Computer Repair',
            is_superuser=True,
            is_staff=True,
            is_active=True, 
            password=self.hashed_password
        )

        self.service_request = ServiceRequest.objects.create(
            name='Service', 
            description='Fix my computer', 
            requested_by=self.customer, 
            owned_by=self.technician
        )
        
        self.part = Part.objects.create(
            name='Hard Drive', 
            description='1TB HDD', 
            quantity_in_stock=10
        )

        self.invoice = Invoice.objects.create(
            name='Invoice', 
            total_amount=100.00
        )

        self.invoice.parts.set([self.part])

        self.invoice.service_requests.set([self.service_request])

        self.repair_log = RepairLog.objects.create(
            start_time='2023-01-18T12:00:00Z',
            end_time='2023-01-18T15:00:00Z',
            service_request=self.service_request,
            technician_notes='Fixed the issue'
        )
        self.address = Address.objects.create(
            address_line1='123 Main St',
            address_line2='Apt 4',
            postal_code='12345',
            city='Cityville',
            state='Stateville',
            country='Countryland'
        )
        self.supplier = Supplier.objects.create(
            name='Supplier1',
            address=self.address,
            phone_number='9876543210'
        )

        self.warehouse = Warehouse.objects.create(
            name='Warehouse1',
            description='Main Warehouse',
            quantity_in_stock=100,
            supplier=self.supplier  # Make sure to set the supplier if needed
        )

        self.comment = Comment.objects.create(
            text='This is a comment',
            posted_by=self.technician
        )

    def get_token(self):
        self.client = Client()


        url = reverse('obtain-token')
       
        data = {
            'username': 'tech@example.com',
            'password': 'Test123.'
        }
   
        response = self.client.post(url, data=data)

        #self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)
        token=content['token']

        headers = {
            'Authorization': f'Token {token}',
        }
        return headers


class ModelTests(BaseTestCase):

 

    def test_models(self):
        self.assertEqual(str(self.customer), 'John Doe ')
        self.assertEqual(str(self.technician), 'Tech Computer Repair')
        self.assertEqual(str(self.technician.email), 'tech@example.com')
        self.assertEqual(str(self.technician.username), 'Tech')
        self.assertEqual(str(self.technician.is_active), 'True')
  
    


class ServiceRequestTests(BaseTestCase):
    
        
    def test_service_request_list_view(self):
        
        response = self.client.get(reverse('service_request_api'),headers=super().get_token())
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
        response = self.client.get(reverse('service_request_detail_api', args=[self.service_request.pk]),headers=super().get_token())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.service_request.name)
        self.assertContains(response, self.service_request.price)
        self.assertContains(response, self.service_request.description)
     
     
    def test_service_request_create_view(self):
        response = self.client.post(reverse('service_request_api'),{'name': 'New service Request', 'description': 'New Description', 'requested_by' :1 ,'owned_by':1},headers=super().get_token())
        self.assertEqual(response.status_code, 201)  # Assuming a successful creation redirects to another page    


    def test_service_request_update_view(self):
        response = self.client.get(reverse('service_request_detail_api', args=[self.service_request.pk]),headers=super().get_token())
        self.assertEqual(response.status_code, 200)

        response = self.client.put(
            reverse('service_request_detail_api', args=[self.service_request.pk]),
            {'name': 'New service Request', 'price':100, 'description': 'New Description', 'requested_by' :1 ,'owned_by':1 },
            content_type='application/json',headers=super().get_token()
        )

        self.assertEqual(response.status_code, 200)  # Assuming a successful update redirects to another page
        
        self.service_request.refresh_from_db()
        self.assertEqual(self.service_request.name, 'New service Request')
        self.assertEqual(self.service_request.price, 100)
        self.assertEqual(self.service_request.description, 'New Description')
        self.assertEqual(self.service_request.requested_by, self.customer)
        self.assertEqual(self.service_request.owned_by, self.technician)
        
    def test_service_request_delete_view(self):
        response = self.client.delete(reverse('service_request_detail_api', args=[self.service_request.pk]),headers=super().get_token())
        self.assertEqual(response.status_code, 204)  # Assuming a successful deletion redirects to another page
        self.assertFalse(ServiceRequest.objects.filter(pk=self.service_request.pk).exists())
        
class InvoiceTests(BaseTestCase):

    def test_invoice_list_view(self):
        response = self.client.get(reverse('invoice_api'),headers=super().get_token())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.invoice.name)
        #self.assertContains(response, self.invoice.price)
        #self.assertContains(response, self.invoice.description)
        self.assertContains(response, self.invoice.total_amount)
      

    def test_invoice_detail_view(self):
        response = self.client.get(reverse('invoice_detail_api', args=[self.invoice.pk]),headers=super().get_token())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.invoice.name)
        #self.assertContains(response, self.invoice.price)
        #self.assertContains(response, self.invoice.description)
        self.assertContains(response, self.invoice.total_amount)


    def test_invoice_create_view(self):
        response = self.client.post(reverse('invoice_api'), {'name': 'Invoice 3241', 'description': 'Fix screen errors', 'requested_by' :1 ,'owned_by':1,'total_amount':100.00, 'parts':1, 'service_requests':1},headers=super().get_token())
        self.assertEqual(response.status_code, 201)  

    def test_invoice_update_view(self):
        response = self.client.get(reverse('invoice_detail_api', args=[self.invoice.pk]),headers=super().get_token())
                                           
        self.assertEqual(response.status_code, 200)

        response = self.client.put(
            reverse('invoice_detail_api', args=[self.invoice.pk]),
            {'name': 'Invoice 123423', 'description': 'Fix laptop drive', 'requested_by' : 1 ,'owned_by':1,'total_amount':200.00,'parts':[1],'service_requests':[1]},
            content_type='application/json',headers=super().get_token()
        )
   
        self.assertEqual(response.status_code, 200) 

        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.name, 'Invoice 123423')
        self.assertEqual(self.invoice.total_amount, 200.00)
        #self.assertEqual(self.invoice.description, 'Fix laptop drive')
        #self.assertEqual(self.invoice.requested_by, self.customer)
        #self.assertEqual(self.invoice.owned_by, self.technician)
        #self.assertEqual(self.invoice.part, self.part)
        #self.assertEqual(self.invoice.service_request, self.service_request)

        
    def test_invoice_delete_view(self):
        response = self.client.delete(reverse('invoice_detail_api', args=[self.invoice.pk]),headers=super().get_token())
        self.assertEqual(response.status_code, 204)  # Assuming a successful deletion redirects to another page
        self.assertFalse(Invoice.objects.filter(pk=self.invoice.pk).exists())

class PartTests(BaseTestCase):

    def test_part_detail_view(self):
        response = self.client.get(reverse('part_detail_api', args=[self.part.pk]),headers=super().get_token())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.part.name)
        self.assertContains(response, self.part.price)
        self.assertContains(response, self.part.description)
        self.assertContains(response, self.part.quantity_in_stock)


    def test_part_create_view(self):
        response = self.client.post(reverse('part_api'), {'name':'Hard Drive', 'description':'1TB HDD', 'quantity_in_stock':10},headers=super().get_token())
        self.assertEqual(response.status_code, 201) 

    def test_part_update_view(self):
        response = self.client.get(reverse('part_detail_api', args=[self.part.pk]),headers=super().get_token())
        self.assertEqual(response.status_code, 200)

        response = self.client.put(
            reverse('part_detail_api', args=[self.part.pk]),
            {'name':'Hard Drive', 'description':'1TB SSD', 'quantity_in_stock':10},
            content_type='application/json',headers=super().get_token()
        )

        self.assertEqual(response.status_code, 200) 

        self.part.refresh_from_db()
        self.assertEqual(self.part.name, 'Hard Drive')
        self.assertEqual(self.part.quantity_in_stock, 10)
        self.assertEqual(self.part.price, 0.00)
        self.assertEqual(self.part.description, '1TB SSD')
        
    def test_part_delete_view(self):
        response = self.client.delete(reverse('part_detail_api', args=[self.part.pk]),headers=super().get_token())
        self.assertEqual(response.status_code, 204)  # Assuming a successful deletion redirects to another page
        self.assertFalse(Part.objects.filter(pk=self.part.pk).exists())

class ServiceTechnicianTests(BaseTestCase):
 
    
    #hashed_password = make_password('Test123...')
        #self.invoice = Invoice.objects.create(name='Invoice', total_amount=100.00, parts=self.part, service_requests=self.service_request)#description='Computer repair services', requested_by=self.customer, owned_by=self.technician)
    def test_service_technician_list_view(self):
        response = self.client.get(reverse('service_technician_api'),headers=super().get_token())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.technician.first_name)
        self.assertContains(response, self.technician.last_name)
        self.assertContains(response, self.technician.email)
        self.assertContains(response, self.technician.phone_number)
        self.assertContains(response, self.technician.specialization)
        

    def test_service_technician_detail_view(self):
        response = self.client.get(reverse('service_technician_detail_api', args=[self.technician.pk]),headers=super().get_token())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.technician.first_name)
        self.assertContains(response, self.technician.last_name)
        self.assertContains(response, self.technician.email)
        self.assertContains(response, self.technician.phone_number)
        self.assertContains(response, self.technician.specialization)
  
       
    def test_token_generation(self):

        response = self.client.get(reverse('service_technician_api'), headers=self.get_token())
        self.assertEqual(response.status_code,200)


    def test_service_technician_create_view(self):

        response = self.client.post(
        reverse('service_technician_api'),
        {
            'first_name': 'Leon',
            'last_name': 'Guy',
            'username': 'tech2@example.com',
            'email': 'tech2@example.com',
            'phone_number': '9876543210',
            'specialization': 'Computer Repair',
            'is_superuser': True,
            'is_staff': True,
            'is_active': True,
            'password': self.hashed_password,
        },
        headers=super().get_token()
        )
        self.assertEqual(response.status_code,201)
     


    def test_service_technician_update_view(self):
        response = self.client.get(reverse('service_technician_detail_api', args=[self.technician.pk]),headers=super().get_token())
        self.assertEqual(response.status_code, 200)

        response = self.client.put(
            reverse('service_technician_detail_api', args=[self.technician.pk]),
            {'first_name':'Rajesh','last_name':'Hrejt', 'username':'tech3@example.com', 'email':'tech3@example.com', 'phone_number':'9876543210','is_superuser':True,'is_staff':True,'is_active':True, 'password':self.hashed_password, 'specialization':'IT programmer'},
            content_type='application/json',headers=super().get_token()
        )

        self.assertEqual(response.status_code, 200) 

        self.technician.refresh_from_db()
        self.assertEqual(self.technician.first_name, 'Rajesh')
        self.assertEqual(self.technician.last_name, 'Hrejt')
        self.assertEqual(self.technician.email, 'tech3@example.com')
        self.assertEqual(self.technician.phone_number, '9876543210')
        self.assertEqual(self.technician.specialization, 'IT programmer')
        
    def test_service_technician_delete_view(self):
        response = self.client.delete(reverse('service_technician_detail_api', args=[self.technician.pk]),headers=super().get_token())
        self.assertEqual(response.status_code, 204)  # Assuming a successful deletion redirects to another page
        self.assertFalse(ServiceTechnician.objects.filter(pk=self.technician.pk).exists())



class CustomerTests(BaseTestCase):
    """def setUp(self):
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
    """
    def test_customer_list_view(self):
        response = self.client.get(reverse('customer_api'),headers=super().get_token())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.customer.name)
        self.assertContains(response, self.customer.surname)
        self.assertContains(response, self.customer.email)
        self.assertContains(response, self.customer.phone_number)

        

    def test_customer_detail_view(self):
        response = self.client.get(reverse('customer_detail_api', args=[self.customer.pk]),headers=super().get_token())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.customer.name)
        self.assertContains(response, self.customer.surname)
        self.assertContains(response, self.customer.email)
        self.assertContains(response, self.customer.phone_number)
        
       

    def test_customer_create_view(self):
        response = self.client.post(reverse('customer_api'), {'name':'Rajesh', 'surname':'Rax', 'email':'rajeshrax@example.com', 'phone_number':'9874343210', 'service_requests':'1'},headers=super().get_token())
        self.assertEqual(response.status_code, 201)  # Assuming a successful creation redirects to another page
       

    def test_customer_update_view(self):
        response = self.client.get(reverse('customer_detail_api', args=[self.customer.pk]),headers=super().get_token())
        self.assertEqual(response.status_code, 200)

        response = self.client.put(
            reverse('customer_detail_api', args=[self.customer.pk]),
            {'name':'Pajet', 'surname':'Hrejt', 'email':'pajethrejt@example.com', 'phone_number':'9874343210', 'service_requests':[1]},
            content_type='application/json',headers=super().get_token()
        )
        #self.assertEqual(response.content,999)
        self.assertEqual(response.status_code, 200)  # Assuming a successful update redirects to another page

        self.customer.refresh_from_db()
        self.assertEqual(self.customer.name, 'Pajet')
        self.assertEqual(self.customer.surname, 'Hrejt')
        self.assertEqual(self.customer.email, 'pajethrejt@example.com')
        self.assertEqual(self.customer.phone_number, '9874343210')


        
    def test_customer_delete_view(self):
        response = self.client.delete(reverse('customer_detail_api', args=[self.customer.pk]),headers=super().get_token())
        self.assertEqual(response.status_code, 204)  # Assuming a successful deletion redirects to another page
        self.assertFalse(Customer.objects.filter(pk=self.customer.pk).exists())


### TO DO ###
#Creating tests of these classes        
"""
class RepairLog(models.Model):

class Warehouse(Part):

class Address(models.Model):

class Comment(models.Model):

class Supplier(models.Model):
"""