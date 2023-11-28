from django.db import models

class CommonInfo(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField(default=0)
    
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
    requested_by = models.ForeignKey('Customer', on_delete=models.CASCADE) #or .SET_NULL, null=True)
    owned_by = models.ForeignKey('ServiceTechnician', on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Service Request'
        verbose_name_plural = 'Service Requests'

    def __str__(self):
        return f"{self.name}"

class Invoice(ServiceRequest):
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.BooleanField(default=False)
     ##TO DO##
    #service_request = models.ForeignKey(ServiceRequest, on_delete=models.SET_NULL, null=True, related_name='invoices')
    #or
    #service_request = models.ForeignKey('ServiceRequest', on_delete=models.SET_NULL, null=True, related_name='+')
    #part =  models.ForeignKey('Part', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'


    def __str__(self):
        return f"{self.name}"

class Part(CommonInfo):
    description = models.CharField(max_length=100)
    quantity_in_stock = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Part'
        verbose_name_plural = 'Parts'

    def __str__(self):
        return f"{self.name}"

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
        return f"{self.name} {self.surname}"
