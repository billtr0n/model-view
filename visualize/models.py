from __future__ import unicode_literals
from django.db import models

# Handles tagging for Simulations to create user-defined queries.
class Tag(models.Model):
    name = models.TextField()
    number_uses = models.IntegerField()
    
class Project(models.Model):
    name = models.TextField()
    number_uses = models.IntegerField()

class Group(models.Model):
    name = models.TextField()
    number_uses = models.IntegerField()
    projects = models.ManyToManyField(Project)

# these fields are only used for referencing, so they will all be forced to
# text type in the database
class Parameters(models.Model):
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
    vp = models.TextField()
    vs = models.TextField()
    rho = models.TextField()
    x1 = models.TextField(null=True, blank=True)
    x2 = models.TextField(null=True, blank=True)
    x3 = models.TextField(null=True, blank=True)
    tn = models.TextField(null=True, blank=True)
    ts = models.TextField(null=True, blank=True)
    pcdep = models.TextField(null=True, blank=True)
    rcrit = models.TextField(null=True, blank=True)
    delts = models.TextField(null=True, blank=True)
    tm0 = models.TextField(null=True, blank=True)
    tmnucl = models.TextField(null=True, blank=True)
    trelax = models.TextField(null=True, blank=True)
    vrup = models.TextField(null=True, blank=True)
    a11 = models.TextField(null=True, blank=True)
    a22 = models.TextField(null=True, blank=True)
    a33 = models.TextField(null=True, blank=True)
    a31 = models.TextField(null=True, blank=True)
    a32 = models.TextField(null=True, blank=True)
    a12 = models.TextField(null=True, blank=True)


# General simulation
class Simulation(Parameters):
    # TODO: These values will come with post request, user and upload_date, think about validating data client side and sending json over
    user = models.CharField(max_length=200, blank=True)
    name = models.CharField(max_length=200, default='', null=True, blank=True)
    upload_date = models.DateTimeField('upload date', blank=True, null=True)
    comments = models.TextField(default='', blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    groups = models.ManyToManyField(Group, blank=True)
    projects = models.ManyToManyField(Project, blank=True)

    def get_fields(self):
        ignore = ['parameters_ptr', 'id'] 
        fields = [(field.name, field.value_to_string(self)) for field in Simulation._meta.fields if field.name not in ignore and field.value_to_string(self)]
        return fields

    def __str__(self):
        return self.name
    
# Stores simulation output data
class Data_Product(models.Model):
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    fieldname = models.CharField(max_length=200)
    data_filename = models.CharField(max_length=200)
    

    def __str__(self):
        return self.simulation.name + ': ' + self.name

