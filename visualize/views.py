from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Simulation

def detail(request, simulation_id):
    simulation = get_object_or_404(Simulation, pk=simulation_id)
    context = {'simulation': simulation}
    return render(request, 'visualize/detail.html', context)

def params(request, simulation_id):
    return HttpResponse("Viewing portal for data products.")

def index(request):
    simulation_list = Simulation.objects.order_by('upload_date')
    context = {'simulation_list': simulation_list}
    return render(request, 'visualize/index.html', context)

