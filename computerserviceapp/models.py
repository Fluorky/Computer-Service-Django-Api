from django.db import models
from django_fsm import FSMField, transition

class CommonInfo(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField(default=0)
    tax = models.DecimalField(default=0,max_digits=10, decimal_places=4)
    
    class Meta:
        abstract = True

class Person(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=11)
    
    class Meta:
        abstract = True



class ServiceRequest(CommonInfo):
    description = models.TextField()
    requested_by = models.ForeignKey('Customer', on_delete=models.CASCADE) 
    owned_by = models.ForeignKey('ServiceTechnician', on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)
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
    
    class Meta:
        verbose_name = 'Part'
        verbose_name_plural = 'Parts'

    def __str__(self):
        return f"{self.name} {self.price} {self.description} {self.quantity_in_stock}"

class Invoice(CommonInfo):
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.BooleanField(default=False)
    service_requests = models.ManyToManyField(ServiceRequest, related_name='invoices')
    parts = models.ManyToManyField(Part, related_name='invoices')

    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'

    def calculate_total_amount(self):
        #To do#
        total_amount_before_tax = 0
        # Calculate tax for ServiceRequests and parts
        """for sr in self.service_requests.all():
            total_amount_before_tax += sr.price * (1 + sr.tax)
    
        for part in self.parts.all():
            total_amount_before_tax += part.price * (1 + part.tax)


        self.total_amount = total_amount_before_tax"""

    def save(self, *args, **kwargs):
        """
        self.calculate_total_amount()
        super().save(*args, **kwargs)"""

    def __str__(self):
        return f"{self.name} {self.total_amount} {self.parts} {self.total_amount} {self.service_requests}"
    


class ServiceTechnician(Person):
   
    specialization = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Service Technician'
        verbose_name_plural = 'Service Technicians'

    def __str__(self):
        return f"{self.name} {self.surname}"

class Customer(Person):
    
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return f"{self.name} {self.surname} {self.address_line1} {self.address_line2} {self.city} {self.country} {self.postal_code} {self.state}"


class RepairLog(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    service_request = models.OneToOneField(ServiceRequest, on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return f"{self.service_request} {self.start_time} {self.end_time}"

class Warehouse(Part):
    quantity_to_order : models.PositiveIntegerField(default=0)
    last_one_order_date : models.DateTimeField()

    def __str__(self):
        return f"{self.name} {self.quantity_to_order} {self.last_one_order_date}"
