# computerserviceapp/tests.py
import json
from django.test import TestCase, Client
from django.urls import reverse
from .models import ServiceRequest, Invoice, Part, ServiceTechnician, Customer, Address, RepairLog, Supplier, Warehouse
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.contrib.auth import get_user_model
from django_fsm import TransitionNotAllowed
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
import subprocess
import unittest


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
            supplier=self.supplier
        )

    def get_token(self):
        self.client = Client()

        url = reverse('obtain-token')

        data = {
            'username': 'tech@example.com',
            'password': 'Test123.'
        }

        response = self.client.post(url, data=data)

        # self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)
        token = content['token']

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
        response = self.client.get(reverse('service_request_api'), headers=super().get_token())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.service_request.name)
        self.assertContains(response, self.service_request.price)
        self.assertContains(response, self.service_request.description)

    def test_models(self):
        service_request = ServiceRequest.objects.get(pk=1)
        self.assertEqual(service_request.state, "new")
        service_request.submit_request()  # Move to 'open' state
        self.assertEqual(service_request.state, "open")
        service_request.start_work()  # Move to 'pending' state
        self.assertEqual(service_request.state, "pending")
        service_request.mark_in_progress()  # Move to 'work_in_progress' state
        self.assertEqual(service_request.state, "work_in_progress")

    def test_service_request_detail_view(self):
        response = self.client.get(reverse('service_request_detail_api', args=[self.service_request.pk]),
                                   headers=super().get_token())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.service_request.name)
        self.assertContains(response, self.service_request.price)
        self.assertContains(response, self.service_request.description)

    def test_service_request_create_view(self):
        response = self.client.post(reverse('service_request_api'),
                                    {'name': 'New service Request', 'description': 'New Description', 'requested_by': 1,
                                     'owned_by': 1}, headers=super().get_token())
        self.assertEqual(response.status_code, 201)  # Assuming a successful creation redirects to another page

    def test_service_request_update_view(self):
        response = self.client.get(reverse('service_request_detail_api', args=[self.service_request.pk]),
                                   headers=super().get_token())
        self.assertEqual(response.status_code, 200)

        response = self.client.put(
            reverse('service_request_detail_api', args=[self.service_request.pk]),
            {'name': 'New service Request', 'price': 100, 'description': 'New Description', 'requested_by': 1,
             'owned_by': 1},
            content_type='application/json', headers=super().get_token()
        )

        self.assertEqual(response.status_code, 200)  # Assuming a successful update redirects to another page

        self.service_request.refresh_from_db()
        self.assertEqual(self.service_request.name, 'New service Request')
        self.assertEqual(self.service_request.price, 100)
        self.assertEqual(self.service_request.description, 'New Description')
        self.assertEqual(self.service_request.requested_by, self.customer)
        self.assertEqual(self.service_request.owned_by, self.technician)

    def test_service_request_delete_view(self):
        response = self.client.delete(reverse('service_request_detail_api', args=[self.service_request.pk]),
                                      headers=super().get_token())
        self.assertEqual(response.status_code, 204)  # Assuming a successful deletion redirects to another page
        self.assertFalse(ServiceRequest.objects.filter(pk=self.service_request.pk).exists())

    def test_str_method(self):
        expected_str = f"{self.service_request.name} {self.service_request.price} {self.service_request.description} {self.service_request.requested_by} {self.service_request.requested_at} {self.service_request.state}"
        self.assertEqual(str(self.service_request), expected_str)

    def test_mark_complete(self):
        self.service_request.submit_request()  # Move to 'open' state
        self.service_request.start_work()  # Move to 'pending' state
        self.service_request.mark_in_progress()  # Move to 'work_in_progress' state
        self.service_request.mark_complete()  # Move to 'closed_complete' state
        self.assertEqual(self.service_request.state, 'closed_complete')

    def test_mark_incomplete(self):
        self.service_request.submit_request()  # Move to 'open' state
        self.service_request.start_work()  # Move to 'pending' state
        self.service_request.mark_in_progress()  # Move to 'work_in_progress' state
        self.service_request.mark_incomplete()  # Move to 'closed_incomplete' state
        self.assertEqual(self.service_request.state, 'closed_incomplete')

    def test_mark_skipped(self):
        self.service_request.submit_request()  # Move to 'open' state
        self.service_request.start_work()  # Move to 'pending' state
        self.service_request.mark_in_progress()  # Move to 'work_in_progress' state
        self.service_request.mark_skipped()  # Move to 'closed_skipped' state
        self.assertEqual(self.service_request.state, 'closed_skipped')

    def test_invalid_transitions(self):
        with self.assertRaises(TransitionNotAllowed):
            self.service_request.mark_complete()

        with self.assertRaises(TransitionNotAllowed):
            self.service_request.mark_incomplete()

        with self.assertRaises(TransitionNotAllowed):
            self.service_request.mark_skipped()


class InvoiceTests(BaseTestCase):

    def test_invoice_list_view(self):
        response = self.client.get(reverse('invoice_api'), headers=super().get_token())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.invoice.name)
        # self.assertContains(response, self.invoice.price)
        # self.assertContains(response, self.invoice.description)
        self.assertContains(response, self.invoice.total_amount)

    def test_invoice_detail_view(self):
        response = self.client.get(reverse('invoice_detail_api', args=[self.invoice.pk]), headers=super().get_token())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.invoice.name)
        # self.assertContains(response, self.invoice.price)
        # self.assertContains(response, self.invoice.description)
        self.assertContains(response, self.invoice.total_amount)

    def test_invoice_create_view(self):
        response = self.client.post(reverse('invoice_api'),
                                    {'name': 'Invoice 3241', 'description': 'Fix screen errors', 'requested_by': 1,
                                     'owned_by': 1, 'total_amount': 100.00, 'parts': 1, 'service_requests': 1},
                                    headers=super().get_token())
        self.assertEqual(response.status_code, 201)

    def test_invoice_update_view(self):
        response = self.client.get(reverse('invoice_detail_api', args=[self.invoice.pk]), headers=super().get_token())

        self.assertEqual(response.status_code, 200)

        response = self.client.put(
            reverse('invoice_detail_api', args=[self.invoice.pk]),
            {'name': 'Invoice 123423', 'description': 'Fix laptop drive', 'requested_by': 1, 'owned_by': 1,
             'total_amount': 200.00, 'parts': [1], 'service_requests': [1]},
            content_type='application/json', headers=super().get_token()
        )

        self.assertEqual(response.status_code, 200)

        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.name, 'Invoice 123423')
        self.assertEqual(self.invoice.total_amount, 200.00)
        # self.assertEqual(self.invoice.description, 'Fix laptop drive')
        # self.assertEqual(self.invoice.requested_by, self.customer)
        # self.assertEqual(self.invoice.owned_by, self.technician)
        # self.assertEqual(self.invoice.part, self.part)
        # self.assertEqual(self.invoice.service_request, self.service_request)

    def test_invoice_delete_view(self):
        response = self.client.delete(reverse('invoice_detail_api', args=[self.invoice.pk]),
                                      headers=super().get_token())
        self.assertEqual(response.status_code, 204)  # Assuming a successful deletion redirects to another page
        self.assertFalse(Invoice.objects.filter(pk=self.invoice.pk).exists())

    def test_str_method(self):
        expected_str = f"{self.invoice.name} {self.invoice.total_amount} {self.invoice.parts} {self.invoice.total_amount} {self.invoice.service_requests}"
        self.assertEqual(str(self.invoice), expected_str)


class PartTests(BaseTestCase):

    def test_part_detail_view(self):
        response = self.client.get(reverse('part_detail_api', args=[self.part.pk]), headers=super().get_token())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.part.name)
        self.assertContains(response, self.part.price)
        self.assertContains(response, self.part.description)
        self.assertContains(response, self.part.quantity_in_stock)

    def test_part_create_view(self):
        response = self.client.post(reverse('part_api'),
                                    {'name': 'Hard Drive', 'description': '1TB HDD', 'quantity_in_stock': 10},
                                    headers=super().get_token())
        self.assertEqual(response.status_code, 201)

    def test_part_update_view(self):
        response = self.client.get(reverse('part_detail_api', args=[self.part.pk]), headers=super().get_token())
        self.assertEqual(response.status_code, 200)

        response = self.client.put(
            reverse('part_detail_api', args=[self.part.pk]),
            {'name': 'Hard Drive', 'description': '1TB SSD', 'quantity_in_stock': 10},
            content_type='application/json', headers=super().get_token()
        )

        self.assertEqual(response.status_code, 200)

        self.part.refresh_from_db()
        self.assertEqual(self.part.name, 'Hard Drive')
        self.assertEqual(self.part.quantity_in_stock, 10)
        self.assertEqual(self.part.price, 0.00)
        self.assertEqual(self.part.description, '1TB SSD')

    def test_part_delete_view(self):
        response = self.client.delete(reverse('part_detail_api', args=[self.part.pk]), headers=super().get_token())
        self.assertEqual(response.status_code, 204)  # Assuming a successful deletion redirects to another page
        self.assertFalse(Part.objects.filter(pk=self.part.pk).exists())

    def test_str_method(self):
        expected_str = f"{self.part.name} {self.part.price} {self.part.description} {self.part.quantity_in_stock}"
        self.assertEqual(str(self.part), expected_str)


class ServiceTechnicianTests(BaseTestCase):

    def test_service_technician_list_view(self):
        response = self.client.get(reverse('service_technician_api'), headers=super().get_token())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.technician.first_name)
        self.assertContains(response, self.technician.last_name)
        self.assertContains(response, self.technician.email)
        self.assertContains(response, self.technician.phone_number)
        self.assertContains(response, self.technician.specialization)

    def test_service_technician_detail_view(self):
        response = self.client.get(reverse('service_technician_detail_api', args=[self.technician.pk]),
                                   headers=super().get_token())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.technician.first_name)
        self.assertContains(response, self.technician.last_name)
        self.assertContains(response, self.technician.email)
        self.assertContains(response, self.technician.phone_number)
        self.assertContains(response, self.technician.specialization)

    def test_token_generation(self):
        response = self.client.get(reverse('service_technician_api'), headers=self.get_token())
        self.assertEqual(response.status_code, 200)

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
        self.assertEqual(response.status_code, 201)

    def test_service_technician_update_view(self):
        response = self.client.get(reverse('service_technician_detail_api', args=[self.technician.pk]),
                                   headers=super().get_token())
        self.assertEqual(response.status_code, 200)

        response = self.client.put(
            reverse('service_technician_detail_api', args=[self.technician.pk]),
            {'first_name': 'Rajesh', 'last_name': 'Hrejt', 'username': 'tech3@example.com',
             'email': 'tech3@example.com', 'phone_number': '9876543210', 'is_superuser': True, 'is_staff': True,
             'is_active': True, 'password': self.hashed_password, 'specialization': 'IT programmer'},
            content_type='application/json', headers=super().get_token()
        )

        self.assertEqual(response.status_code, 200)

        self.technician.refresh_from_db()
        self.assertEqual(self.technician.first_name, 'Rajesh')
        self.assertEqual(self.technician.last_name, 'Hrejt')
        self.assertEqual(self.technician.email, 'tech3@example.com')
        self.assertEqual(self.technician.phone_number, '9876543210')
        self.assertEqual(self.technician.specialization, 'IT programmer')

    def test_service_technician_delete_view(self):
        response = self.client.delete(reverse('service_technician_detail_api', args=[self.technician.pk]),
                                      headers=super().get_token())
        self.assertEqual(response.status_code, 204)  # Assuming a successful deletion redirects to another page
        self.assertFalse(ServiceTechnician.objects.filter(pk=self.technician.pk).exists())


class CustomerTests(BaseTestCase):

    def test_customer_list_view(self):
        response = self.client.get(reverse('customer_api'), headers=super().get_token())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.customer.name)
        self.assertContains(response, self.customer.surname)
        self.assertContains(response, self.customer.email)
        self.assertContains(response, self.customer.phone_number)

    def test_customer_detail_view(self):
        response = self.client.get(reverse('customer_detail_api', args=[self.customer.pk]), headers=super().get_token())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.customer.name)
        self.assertContains(response, self.customer.surname)
        self.assertContains(response, self.customer.email)
        self.assertContains(response, self.customer.phone_number)

    def test_customer_create_view(self):
        response = self.client.post(reverse('customer_api'),
                                    {'name': 'Rajesh', 'surname': 'Rax', 'email': 'rajeshrax@example.com',
                                     'phone_number': '9874343210', 'service_requests': '1'},
                                    headers=super().get_token())
        self.assertEqual(response.status_code, 201)  # Assuming a successful creation redirects to another page

    def test_customer_update_view(self):
        response = self.client.get(reverse('customer_detail_api', args=[self.customer.pk]), headers=super().get_token())
        self.assertEqual(response.status_code, 200)

        response = self.client.put(
            reverse('customer_detail_api', args=[self.customer.pk]),
            {'name': 'Pajet', 'surname': 'Hrejt', 'email': 'pajethrejt@example.com', 'phone_number': '9874343210',
             'service_requests': [1]},
            content_type='application/json', headers=super().get_token()
        )
        # self.assertEqual(response.content,999)
        self.assertEqual(response.status_code, 200)  # Assuming a successful update redirects to another page

        self.customer.refresh_from_db()
        self.assertEqual(self.customer.name, 'Pajet')
        self.assertEqual(self.customer.surname, 'Hrejt')
        self.assertEqual(self.customer.email, 'pajethrejt@example.com')
        self.assertEqual(self.customer.phone_number, '9874343210')

    def test_customer_delete_view(self):
        response = self.client.delete(reverse('customer_detail_api', args=[self.customer.pk]),
                                      headers=super().get_token())
        self.assertEqual(response.status_code, 204)  # Assuming a successful deletion redirects to another page
        self.assertFalse(Customer.objects.filter(pk=self.customer.pk).exists())


class RepairLogTests(TestCase):
    def setUp(self):
        self.repair_log = RepairLog.objects.create(
            start_time=timezone.datetime(2023, 1, 18, 12, 0, tzinfo=timezone.utc),
            end_time=timezone.datetime(2023, 1, 18, 15, 0, tzinfo=timezone.utc),
            service_request=None,  # insert a ServiceRequest instance if needed
            technician_notes='Fixed the issue'
        )

    def test_retrieve_repair_log(self):
        repair_log = RepairLog.objects.get(id=self.repair_log.id)
        expected_start_time = timezone.datetime(2023, 1, 18, 12, 0, tzinfo=timezone.utc)
        self.assertEqual(repair_log.start_time, expected_start_time)

    def test_create_repair_log(self):
        self.assertTrue(isinstance(self.repair_log, RepairLog))

    def test_update_repair_log(self):
        self.repair_log.technician_notes = 'Replaced faulty part'
        self.repair_log.save()
        updated_repair_log = RepairLog.objects.get(id=self.repair_log.id)
        self.assertEqual(updated_repair_log.technician_notes, 'Replaced faulty part')

    def test_delete_repair_log(self):
        self.repair_log.delete()
        self.assertFalse(RepairLog.objects.filter(id=self.repair_log.id).exists())

    def test_str_method(self):
        expected_str = f"RepairLog {self.repair_log.id} from {self.repair_log.start_time} to {self.repair_log.end_time} {self.repair_log.service_request} {self.repair_log.text} {self.repair_log.posted_by} {self.repair_log.posted_at}"
        self.assertEqual(str(self.repair_log), expected_str)


class WarehouseTests(TestCase):
    def setUp(self):
        self.warehouse = Warehouse.objects.create(
            name='Warehouse1',
            description='Main Warehouse',
            quantity_in_stock=100,
            supplier=None,
        )

    def test_create_warehouse(self):
        self.assertTrue(isinstance(self.warehouse, Warehouse))

    def test_retrieve_warehouse(self):
        warehouse = Warehouse.objects.get(id=self.warehouse.id)
        self.assertEqual(warehouse.name, 'Warehouse1')

    def test_update_warehouse(self):
        self.warehouse.quantity_in_stock = 200
        self.warehouse.save()
        updated_warehouse = Warehouse.objects.get(id=self.warehouse.id)
        self.assertEqual(updated_warehouse.quantity_in_stock, 200)

    def test_delete_warehouse(self):
        self.warehouse.delete()
        self.assertFalse(Warehouse.objects.filter(id=self.warehouse.id).exists())

    def test_str_method(self):
        expected_str = f"{self.warehouse.name}"
        self.assertEqual(str(self.warehouse), expected_str)


class AddressTests(TestCase):
    def setUp(self):
        self.address = Address.objects.create(
            address_line1='123 Main St',
            address_line2='Apt 4',
            postal_code='12345',
            city='Cityville',
            state='Stateville',
            country='Countryland'
        )

    def test_create_address(self):
        self.assertTrue(isinstance(self.address, Address))

    def test_retrieve_address(self):
        address = Address.objects.get(id=self.address.id)
        self.assertEqual(address.city, 'Cityville')

    def test_update_address(self):
        self.address.postal_code = '54321'
        self.address.save()
        updated_address = Address.objects.get(id=self.address.id)
        self.assertEqual(updated_address.postal_code, '54321')

    def test_delete_address(self):
        self.address.delete()
        self.assertFalse(Address.objects.filter(id=self.address.id).exists())

    def test_str_method(self):
        expected_str = f"{self.address.address_line1} {self.address.address_line2} {self.address.postal_code} {self.address.city} {self.address.state} {self.address.country}"
        self.assertEqual(str(self.address), expected_str)


class SupplierTests(TestCase):
    def setUp(self):
        address = Address.objects.create(
            address_line1='123 Main St',
            address_line2='Apt 4',
            postal_code='12345',
            city='Cityville',
            state='Stateville',
            country='Countryland'
        )
        self.supplier = Supplier.objects.create(
            name='Example Supplier',
            address=address,
            phone_number='9876543210'
        )

    def test_supplier_has_address(self):
        supplier = Supplier.objects.get(id=self.supplier.id)
        self.assertIsNotNone(supplier.address)

    def test_create_supplier(self):
        self.assertTrue(isinstance(self.supplier, Supplier))

    def test_retrieve_supplier(self):
        supplier = Supplier.objects.get(id=self.supplier.id)
        self.assertEqual(supplier.phone_number, '9876543210')

    def test_update_supplier(self):
        self.supplier.phone_number = '1234567890'
        self.supplier.save()
        updated_supplier = Supplier.objects.get(id=self.supplier.id)
        self.assertEqual(updated_supplier.phone_number, '1234567890')

    def test_delete_supplier(self):
        self.supplier.delete()
        self.assertFalse(Supplier.objects.filter(id=self.supplier.id).exists())

    def test_str_method(self):
        expected_str = f"{self.supplier.name} {self.supplier.address} {self.supplier.phone_number}" """{self.contact_person}"""
        self.assertEqual(str(self.supplier), expected_str)


class ServiceTechnicianManagerTests(TestCase):

    def setUp(self):
        self.user_model = get_user_model()
        self.manager = self.user_model.objects

    def test_create_user_with_email_successful(self):
        email = 'test@example.com'
        password = 'testpassword123'
        user = self.manager.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_without_email_raises_error(self):
        with self.assertRaises(ValueError) as context:
            self.manager.create_user(email=None, password='testpassword123')

        self.assertEqual(str(context.exception), 'The Email field must be set')

    def test_create_superuser_with_email_successful(self):
        email = 'super@example.com'
        password = 'superpassword123'
        user = self.manager.create_superuser(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_superuser_with_default_fields(self):
        email = 'super@example.com'
        password = 'superpassword123'
        user = self.manager.create_superuser(email=email, password=password)

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class LoginViewTests(APITestCase):

    # def setUp(self):
    #     self.user = ServiceTechnician.objects.create_user(username='testuser', specialization='IT', email='testuser@example.com', password='testpass')
    #     self.url = reverse('login')
    #     self.token_url = reverse('obtain-token')
    #     response = self.client.post(self.token_url, {'username': 'testuser@example.com', 'password': 'testpass'}, format='json')
    #     self.token = response.data['token']
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)  # Set the token for future requests
    #
    # def test_login_success(self):
    #     response = self.client.post(self.url, {'username': 'testuser@example.com', 'password': 'testpass'}, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIn('token', response.data)
    #
    # def test_login_failure(self):
    #     response = self.client.post(self.url, {'username': 'testuser', 'password': 'wrongpass'}, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #     self.assertIn('detail', response.data)
    #     self.assertEqual(response.data['detail'], 'Invalid credentials')
    #
    # def test_login_token_creation(self):
    #     print('Running test_login_token_creation')
    #     # Ensure no token exists for the user
    #     Token.objects.filter(user=self.user).delete()
    #     with self.assertRaises(Token.DoesNotExist):
    #         Token.objects.get(user=self.user)
    #
    #     # Authenticate and create token
    #     response = self.client.post(self.url, {'username': 'testuser@example.com', 'password': 'testpass'},
    #                                 format='json')
    #     print('Response status code:', response.status_code)
    #     print('Response data:', response.data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIn('token', response.data)
    #
    #     # Check that the token is created
    #     token = Token.objects.get(user=self.user)
    #     self.assertEqual(response.data['token'], token.key)

    def setUp(self):
        self.user = ServiceTechnician.objects.create_user(
            username='testuser',
            specialization='IT',
            email='testuser@example.com',
            password='testpass'
        )
        self.url = reverse('login')

    def test_login_success(self):
        # print('Running test_login_success')
        response = self.client.post(self.url, {'username': 'testuser@example.com', 'password': 'testpass'},
                                    format='json')
        # print('Response status code:', response.status_code)
        # print('Response data:', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_failure(self):
        # print('Running test_login_failure')
        response = self.client.post(self.url, {'username': 'testuser@example.com', 'password': 'wrongpass'},
                                    format='json')
        # print('Response status code:', response.status_code)
        # print('Response data:', response.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Invalid credentials')

    def test_login_token_creation(self):
        # print('Running test_login_token_creation')
        # Ensure no token exists for the user
        Token.objects.filter(user=self.user).delete()
        with self.assertRaises(Token.DoesNotExist):
            Token.objects.get(user=self.user)

        # Authenticate and create token
        response = self.client.post(self.url, {'username': 'testuser@example.com', 'password': 'testpass'},
                                    format='json')
        # print('Response status code:', response.status_code)
        # print('Response data:', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

        # Check that the token is created
        token = Token.objects.get(user=self.user)
        self.assertEqual(response.data['token'], token.key)


class CreateUserViewTests(APITestCase):

    def setUp(self):
        self.url = reverse('create_user')
        self.client = APIClient()

    def test_create_user_success(self):
        data = {
            'username': 'newuser',
            'password': 'newpass',
            'specialization' : 'IT',
            'email': 'newuser@example.com'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'User created successfully')

    def test_create_user_missing_fields(self):
        response = self.client.post(self.url, {'username': 'newuser'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Username email and password are required')

    def test_create_user_username_taken(self):
        ServiceTechnician.objects.create_user(username='takenuser',  email='takenuser@example.com', password='testpass')
        data = {
            'username': 'takenuser',
            'password': 'newpass',
            'email': 'newuser@example.com'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Username already taken')

    def test_create_user_email_taken(self):
        ServiceTechnician.objects.create_user(username='newuser2', specialization='IT', email='taken@example.com', password='testpass')
        data = {
            'username': 'newuser',
            'password': 'newpass',
            'email': 'taken@example.com'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Email already taken')


class CustomAPIViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = ServiceTechnician.objects.create_user(username='testuser', specialization='IT', email='testuser@example.com', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('address_api')  # Ensure the URL name matches your URLconf

    def test_post_valid_data(self):
        data = {
            'address_line1': '123 Main St',
            'address_line2': 'Apt 4',
            'postal_code': '12345',
            'city': 'Cityville',
            'state': 'Stateville',
            'country': 'Countryland',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_invalid_data(self):
        data = {
            'invalid_field': 'value'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestManageScript(unittest.TestCase):
    def test_manage_script_runs(self):
        # Run the management script and capture the output and error streams
        process = subprocess.Popen(
            ["python", "manage.py", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        stdout, stderr = process.communicate()

        # Check if there was no error running the script
        self.assertEqual(process.returncode, 0)

        # Check if the output contains expected information (for example, Django version)
        self.assertIn("4.2.7\n", stdout)