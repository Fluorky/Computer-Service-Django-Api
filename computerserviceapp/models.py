from django.db import models
from django_fsm import FSMField, transition
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class BasicInfo(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        abstract = True

class CommonInfo(BasicInfo):
    price = models.PositiveIntegerField(default=0)
    tax = models.DecimalField(default=0,max_digits=10, decimal_places=4)
    
    class Meta:
        abstract = True

class Person(models.Model):
    name = models.CharField(max_length=100, null=True)
    surname = models.CharField(max_length=100,null=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=11,null=True)
    
    class Meta:
        abstract = True


class ServiceRequest(CommonInfo):
    description = models.TextField()
    requested_by = models.ForeignKey('Customer', on_delete=models.CASCADE) 
    owned_by = models.ForeignKey('ServiceTechnician', on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)
    completion_deadline = models.DateTimeField(null=True)
    priority = models.IntegerField(default=0)
    billing_address = models.ForeignKey('Address', on_delete=models.CASCADE, related_name='service_request_billing_address',null=True)
    shipping_address = models.ForeignKey('Address', on_delete=models.CASCADE, related_name='service_request_shipping_address',null=True)
       # Define FSMField to manage the state
    state = FSMField(default='new')#,protected=True)

    class Meta:
        verbose_name = 'Service Request'
        verbose_name_plural = 'Service Requests'

    def __str__(self):
        return f"{self.name} {self.price} {self.description} {self.requested_by} {self.requested_at} {self.state}"
    
     # Define state transitions
    @transition(field=state, source='new', target='open')
    def submit_request(self):
        pass

    @transition(field=state, source='open', target='pending')
    def start_work(self):
        pass

    @transition(field=state, source=['new', 'pending'], target='work_in_progress')
    def mark_in_progress(self):
        pass

    @transition(field=state, source=['work_in_progress', 'pending'], target='closed_complete')
    def mark_complete(self):
        pass

    @transition(field=state, source=['work_in_progress', 'pending'], target='closed_incomplete')
    def mark_incomplete(self):
        pass

    @transition(field=state, source=['work_in_progress', 'pending'], target='closed_skipped')
    def mark_skipped(self):
        pass

class Part(CommonInfo):
    description = models.CharField(max_length=100)
    quantity_in_stock = models.PositiveIntegerField(default=0)
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE,null=True)
    
    class Meta:
        verbose_name = 'Part'
        verbose_name_plural = 'Parts'

    def __str__(self):
        return f"{self.name} {self.price} {self.description} {self.quantity_in_stock}"

class Invoice(BasicInfo):
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    payment_status = models.BooleanField(default=False)
    service_requests = models.ManyToManyField(ServiceRequest, related_name='invoices')
    parts = models.ManyToManyField(Part, related_name='invoices')
    billing_address = models.ForeignKey('Address', on_delete=models.CASCADE, related_name='invoice_billing_address',null=True)
    shipping_address = models.ForeignKey('Address', on_delete=models.CASCADE, related_name='invoice_shipping_address',null=True)

    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'

    def calculate_total_tax(self):
        return sum(part.price * part.tax for part in self.parts.all()) + sum(sr.price * sr.tax for sr in self.service_requests.all())

    def calculate_total_amount_without_tax(self):
        return sum(part.price for part in self.parts.all()) + sum(sr.price for sr in self.service_requests.all())

    def calculate_total_amount_with_tax(self):
        return self.calculate_total_amount_without_tax() + self.calculate_total_tax()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.total_amount = self.calculate_total_amount_with_tax()

    def __str__(self):
       return f"{self.name} {self.total_amount} {self.parts} {self.total_amount} {self.service_requests}"



class ServiceTechnicianManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class ServiceTechnician(AbstractUser):
    specialization = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  
    password = models.CharField(max_length=128) 
    phone_number = models.CharField(max_length=11,null=True)
    USERNAME_FIELD = 'email'  # Use email as the username field
    date_joined = models.DateTimeField(default=timezone.now)
    REQUIRED_FIELDS = ['username']  # Add any additional required fields

    class Meta:
        verbose_name = 'Service Technician'
        verbose_name_plural = 'Service Technicians'


    objects = ServiceTechnicianManager()

    def __str__(self):
        return f"{self.username} {self.specialization}" 


class Customer(Person):

    address = models.ForeignKey('Address', on_delete=models.CASCADE,null=True)
    service_requests = models.ManyToManyField(ServiceRequest, related_name='customers')

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):  
        return f"{self.name} {self.surname} "
       


class RepairLog(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    service_request = models.OneToOneField(ServiceRequest, on_delete=models.SET_NULL,null=True)
    technician_notes = models.TextField(null=True)

    def __str__(self):
        return f"{self.service_request} {self.start_time} {self.end_time}"

class Warehouse(Part):
    quantity_to_order : models.PositiveIntegerField(default=0)
    last_one_order_date : models.DateTimeField()

    def __str__(self):
        return f"{self.name} {self.quantity_to_order} {self.last_one_order_date}"

class Address(models.Model):
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.address_line1} {self.address_line2} {self.postal_code} {self.city} {self.state} {self.country}"

class Comment(models.Model):
    text = models.TextField()
    posted_by = models.ForeignKey('ServiceTechnician', on_delete=models.CASCADE,null=True)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text} {self.posted_by} {self.posted_at}"
    
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    #contact_person = models.ForeignKey('Person', on_delete=models.CASCADE)
    address = models.ForeignKey('Address', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} {self.address} {self.phone_number}" """{self.contact_person}""" 
