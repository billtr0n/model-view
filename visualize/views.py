#python includes
import os, logging

# django includes
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

# my includes
from .models import Simulation
from .tasks import process_and_upload_simulations_task, test

""" upload method will accept a list of folders that need to be operated on. these should be transfered to the server already. 
    after they are done uploading they will redirect to models. new models will be visible from models page. """
def upload(request):
    if request.method == 'POST':
        if request.is_ajax():
            post = request.POST.get('post');
            clean_post = _cleanse_post( post )
            if clean_post:
                for file in clean_post:
                    print file
                    process_and_upload_simulations_task.delay( file )
                response = { 'status' : 'success' }
            else:
                response = { 'status' : 'failed' }
            return JsonResponse(response)
    return render(request, 'visualize/upload.html')

def detail(request, simulation_id):
    simulation = get_object_or_404(Simulation, pk=simulation_id)
    context = {'simulation': simulation}
    return render(request, 'visualize/detail.html', context)

def params(request, simulation_id):
    return HttpResponse("Viewing portal for data products.")

def index(request):
    simulation_list = Simulation.objects.order_by('upload_date')
    context = {'simulation_list': simulation_list}
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

