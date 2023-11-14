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
    # details would go here
    pass

class Invoice(ServiceRequest):
     # details would go here
     pass

class Part(CommonInfo):
    # details would go here
    pass

class ServiceTechnicina(Person):
    # details would go here
    pass
class Customer(Person):
    # details would go here
    pass

