from __future__ import unicode_literals
from django.db import models
# these fields are only used for referencing, so they will all be forced to
# 
class Parameters( models.Model ):
    bc1 = models.TextField() 
    bc2 = models.TextField()
    delts = models.TextField()
    dt = models.TextField()
    dx = models.TextField() 
    eplasticity = models.TextField()
    faultnormal = models.TextField()
    friction = models.TextField()
    ihypo = models.TextField()
    np3 = models.TextField()
    npml = models.TextField()
    nt = models.TextField()
    nn = models.TextField()
    rundir = models.TextField()
    pcdep = models.TextField(null=True, blank=True)
    rcrit = models.TextField(null=True, blank=True)
    delts = models.TextField(null=True, blank=True)
    tm0 = models.TextField(null=True, blank=True)
    tmnucl = models.TextField(null=True, blank=True)
    trelax = models.TextField(null=True, blank=True)


# General simulation
class Simulation( models.Model ):
    # TODO: These values will come with post request, user and upload_date, think about validating data client side and sending json over
    user = models.CharField(max_length=200, blank=True)
    name = models.CharField(max_length=200, default='', null=True, blank=True)
    upload_date = models.DateTimeField('upload date', blank=True, null=True)
    comments = models.TextField(default='', blank=True)
    parameters = models.OneToOneField( Parameters )

    def get_fields(self):
        ignore = ['parameters_ptr', 'id'] 
        fields = [(field.name, field.value_to_string(self)) for field in Simulation._meta.fields if field.name not in ignore and field.value_to_string(self)]
        return fields

    def __str__(self):
        return self.name
    
# Stores simulation output data
class Data_Product( models.Model ):
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    fieldname = models.CharField(max_length=200)
    data_filename = models.CharField(max_length=200)
    io = models.CharField(max_length=6)
    file = models.CharField(max_length=200)
    field = models.CharField(max_length=200)
    val = models.CharField(max_length=200, null=True, blank=True)
    shape = models.CharField(max_length=200, null=True, blank=True)
    indices = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.simulation.name + ': ' + self.name


# Handles tagging for Simulations to create user-defined queries.
class Tag(models.Model):
    name = models.TextField()
    number_uses = models.IntegerField()
    simulation = models.ManyToManyField( Simulation )