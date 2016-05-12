from __future__ import unicode_literals
from django.db import models

# Create your models here.
class Simulation(models.Model):
    user = models.CharField(max_length=200)
    name = models.CharField(max_length=200, default='unknown')
    upload_date = models.DateTimeField('upload date')

    def __str__(self):
        return self.name
    
class Data_Product(models.Model):
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE, blank=False, default='unknown')
    fieldname = models.CharField(max_length=200)
    filename = models.CharField(max_length=200)

    def __str__(self):
        return self.simulation.name + ': ' + self.fieldname


    
    
