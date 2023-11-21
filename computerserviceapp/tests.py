from django.test import TestCase

from django.test import TestCase
from .models import Part

class PartTestClass(TestCase):
    def setUp(self):       
        Part.objects.create(id=30, name="CPU I7 14700K", price=32, description = "INTEL CPU", quantity_in_stock = 10)
    def test_1(self):
        cpu = Part.objects.get(id=30)
        self.assertEqual(cpu.quantity_in_stock,32)
               
    def test_2(self):
        cpu = Part.objects.get(id=30)
        self.assertEqual(cpu.price,32)

##TO DO##
# Creating tests here.
