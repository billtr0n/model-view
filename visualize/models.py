from __future__ import unicode_literals
from django.db import models
# these fields are only used for referencing, so they will all be forced to
# 

# General simulation
class Simulation( models.Model ):
    # TODO: These values will come with post request, user and upload_date, think about validating data client side and sending json over
    user = models.CharField(max_length=200, blank=True)
    name = models.CharField(max_length=200, default='', null=True, blank=True, unique=True)
    upload_date = models.DateTimeField('upload date', blank=True, null=True)
    comments = models.TextField(default='', blank=True)
    
    def get_fields(self):
        ignore = ['parameters_ptr', 'id'] 
        fields = [(field.name, field.value_to_string(self)) for field in Simulation._meta.fields if field.name not in ignore and field.value_to_string(self)]
        return fields

    def unicode(self):
        return self.name
    
# Stores simulation output data
class Simulation_Input( models.Model ):
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE)
    file = models.CharField(max_length=200, null=True, blank=True)
    fieldname = models.CharField(max_length=200)
    val = models.CharField(max_length=200, null=True, blank=True)

class Simulation_Output( models.Model ):
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE)
    file = models.CharField(max_length=200)
    field = models.CharField(max_length=200)
    shape = models.CharField(max_length=200)
    indices = models.CharField(max_length=200)

    def unicode(self):
        return self.simulation.name + ': ' + self.field


# Handles tagging for Simulations to create user-defined queries.
class Tag(models.Model):
    name = models.TextField()
    simulation = models.ManyToManyField( Simulation )

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
    simulation = models.OneToOneField( Simulation, on_delete=models.CASCADE )

class Rupture_Parameters( models.Model ):
    simulation = models.OneToOneField( Simulation, on_delete=models.CASCADE )
    fault_extent = models.TextField()
    magnitude = models.TextField()
    del_tau = models.TextField()

