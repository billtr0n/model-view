#python includes
import os, logging

# django includes
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.exceptions import ObjectDoesNotExist

# my includes
from .models import Simulation, Parameters, Rupture_Parameters,OnePoint,Figure
from .models import Simulation_Input, Simulation_Output
from .tasks import process_and_upload_simulations_task

""" upload method will accept a list of folders that need to be operated on. these should be transfered to the server already. 
    after they are done uploading they will redirect to models. new models will be visible from models page. """
def upload(request):
    if request.method == 'POST':
        if request.is_ajax():
            post = request.POST.get('post');
            clean_post = _cleanse_post( post )
            if clean_post:
                for file in clean_post:
                    process_and_upload_simulations_task.delay( file )
                response = { 'status' : 'success' }
            else:
                response = { 'status' : 'failed' }
            return JsonResponse(response)
    return render(request, 'visualize/upload.html')

def detail(request, simulation_id):
    # probably a better way to grab shit from the database
    # maybe wrap into single massive query
    simulation_list = Simulation.objects.order_by('upload_date')
    simulation = get_object_or_404(Simulation, pk=simulation_id)
    parameters = _get_or_none(Parameters, simulation=simulation)
    rupture = _get_or_none(Rupture_Parameters, simulation=simulation)
    one_point = _get_or_none(OnePoint, simulation=simulation)
    inp = _get_many_or_none(Simulation_Input, simulation=simulation)
    outp = _get_many_or_none(Simulation_Output, simulation=simulation)
    figs = _get_figures(simulation)
    context = {
               'list': simulation_list, 
               'par': parameters, 
               'sim': simulation,
               'rup': rupture, 
               'one_point': one_point, 
               'figs': figs, 
               'inp': inp, 
               'outp': outp
              }
    return render(request, 'visualize/detail.html', context)

def index(request):
    simulation_list = Simulation.objects.order_by('upload_date')
    context = {'simulation_list': simulation_list }
    return render( request, 'visualize/index.html', context )


def _cleanse_post( post ):
    """ checks whether the input files sent are valid. aka exist in specified location on server. """
    exists = True

    # shortcut, obvious first.
    if not post:
        return False

    # list of files to return
    out = []

    # maybe it has several files
    try:
        files = post.split('\n')
        for f in files:
            if f and not os.path.isdir( f ):
                exists = False
            elif f and os.path.isdir( f ):
                out.append( f )

    # be more specific
    except Exception as e:
        logging.info('unable to iterate on post, trying as single file.\nerror msg: %s' % str(e))
        # maybe it has one file
        try:
            if not os.path.isdir( post ):
                exists = False
            else:
                out.append( f )
        except Exception as e:
            logging.error('unable to use as single file. failing.\nerror msg: %s' % str(e))
            exists = False

    # phew, made it thru
    logging.info('exists: %s' % str(exists))
    return out

def _get_or_none( model_class, **kwargs ):
    try:
        query = model_class.objects.get( **kwargs )
    # could check if object does not exist, but we want none if it doesn't work
    except:
        query = None
    return query

def _get_many_or_none( model_class, **kwargs ):
    try:
        query = model_class.objects.filter( **kwargs )
    except:
        query = None
    return query

def _get_figures( fk ):
    try:
        query = Figure.objects.filter(simulation=fk, active=True).values('file_path','name')
    except:
        query = None
    return query