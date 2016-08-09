from django.contrib import admin
from .models import Simulation,Tag,Simulation_Output,Simulation_Input,Parameters

# Register your models here.
admin.site.register(Simulation)
admin.site.register(Tag)
admin.site.register(Simulation_Output)
admin.site.register(Simulation_Input)
admin.site.register(Parameters)
