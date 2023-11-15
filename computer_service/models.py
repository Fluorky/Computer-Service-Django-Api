from django.db import models

class CommonInfo(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()

    class Meta:
        abstract = True


class Person(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True

class ServiceRequest(CommonInfo):
    description = models.TextField()
    requested_by = models.ForeignKey('Customer', on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Service Request'
        verbose_name_plural = 'Service Requests'

class Invoice(ServiceRequest):
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'

class Part(CommonInfo):
    description = models.CharField(max_length=100)
    quantity_in_stock = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Part'
        verbose_name_plural = 'Parts'

class ServiceTechnician(Person):
    surname = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Service Technician'
        verbose_name_plural = 'Service Technicians'

class Customer(Person):
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
