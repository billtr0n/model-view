from celery import shared_task
from celery.utils.log import get_task_logger

@shared_task(name='test_task')
def test(param):
    return 'tasked executed with params %s' % param


@shared_task(name = "process_simulations_task")
def process_and_upload_simulations_task( file ):
    """Container task used to process an entire dynamic rupture simulation.  Used when processing multiple
       simulations, so task queue does not get absolutely massive.

    General steps:
        1) Plot kinematic fields
        2) Create one-point statistics
            - histogram using ~100,000 points where rupture velocity is subshear and outside nucleation zone
        and outside velocity weakening zone, the latter will be applied later during the kinematic modeling phase.
        3) Create CSV files for analysis in R based on previous 100,000 points 
            - psv, vrup, slip, mu0
        4) Generate markdown file showing kinematic fields, and summary of one-point statistics
    

    Args:
        params (dict) : contains all parameters necessary for tasks
    Returns:
        Success. Task is expected to fail elegantly and report any issues to the log, but if for some reason
        it does not this function will return false.
    """
    

    import os, shutil, subprocess
   
    import numpy as np
    import pandas as pd

    from util import compute_rupture_velocity, plot_2d_image 

    from .forms import SimulationForm, ParametersForm, RuptureParametersForm, OnePointForm, FigureForm, SimulationInputForm, SimulationOutputForm
    from .models import Simulation

    """ Model setup, this will return false in ready method of class when written """
    # parse simulation details into dict
    logger = get_task_logger(__name__)
    home_dir = os.path.dirname(os.path.realpath(__file__)) 
    script_dir = os.path.join(home_dir, 'utils')
    cwd = file
    try:
        simulation = _parse_simulation_details( cwd )
        # get necessary params for evaluation
    except:
        logger.error('unable to parse meta.py file.')
        return

    # copy necessary files
    # copy entire utils directory 
    try:
        # temporary until i get fortran codes implemented
        shutil.copy( os.path.join(script_dir, 'bbp1d_1250_dx_25.asc'), cwd )
        shutil.copy( os.path.join(script_dir, 'analysis.R'), cwd )
        shutil.copy( os.path.join(script_dir, 'nscore.R'), cwd )
    except Exception as e:
        print str(e)
        return 

    try:
        nn = simulation['parameters']['nn']
        cwd = cwd
        nx = nn[0]
        nz = nn[1]
        dx = simulation['parameters']['dx'][0]
        ihypo = np.array(simulation['parameters']['ihypo'])*dx
        outdir = os.path.join(cwd, 'out')
        figdir = os.path.join(cwd, 'figs')
        datadir = os.path.join(cwd, 'data')
        if not os.path.exists( figdir ):
            os.mkdir( figdir )
        if not os.path.exists( datadir ):
            os.mkdir( datadir )
    except Exception as e:
        print str(e)
        return

    # this should be more general to plot any/all of the fields output
    # interface with fieldnames.py to write little blurb about each fig
    # for now, these can be hard coded.
    logger.info('beginning work on %s' % outdir)
    files = {
        'su1'  : os.path.join( outdir, 'su1' ),
        'su2'  : os.path.join( outdir, 'su2' ),
        'trup' : os.path.join( outdir, 'trup' ),
        'psv'  : os.path.join( outdir, 'psv' ),
        'tsm'  : os.path.join( outdir, 'tsm' ),
        'tnm'  : os.path.join( outdir, 'tnm' ),
    }
    logger.info( 'working with files: %s' % ', '.join( files.keys() ) )

    # load files into dict
    # TODO: change this functionality to accept any field in simulation['fieldio']['inputs']
    # TODO: Make simulation a class. right now i didn't, bc it just stores data no functionality needed
    try:
        ex = dx * nx
        ez = dx * nz
        x = np.arange( 0, ex, dx )
        z = np.arange( 0, ez, dx )
        xx, zz = np.meshgrid( x, z )
        material = np.loadtxt( os.path.join(cwd, 'bbp1d_1250_dx_25.asc') )*1e3
        dtype = simulation['parameters']['dtype']
        data = {
            'x'    : xx,
            'z'    : zz,
            'su1'  : np.fromfile( files['su1'], dtype=dtype ).reshape([ nz, nx ]),
            'su2'  : np.fromfile( files['su2'], dtype=dtype ).reshape([ nz, nx ]),
            'trup' : np.fromfile( files['trup'], dtype=dtype ).reshape([ nz, nx ]),
            'psv'  : np.fromfile( files['psv'], dtype=dtype ).reshape([ nz, nx ]),
            'tsm'  : np.fromfile( files['tsm'], dtype=dtype, count=nx*nz ).reshape([ nz, nx ]) / 1e6, # read initial shear stresses
            'tnm'  : np.fromfile( files['tnm'], dtype=dtype, count=nx*nz ).reshape([ nz, nx ]) / 1e6, # read initial normal stresses
        }
        
        # calculate some things
        tsm_field = (item for item in simulation['fieldio']['outputs'] if item['field'] == "tsm").next()
        vs_field = (item for item in simulation['fieldio']['inputs'] if item['field'] == "vs").next()
        # at some point i want to be able to 
        if vs_field['val'] != "":
            vs = float(vs_field['val'])
            logger.info('using vs %f' % vs)
        else:
            vs = material[:-1,2].repeat(nx).reshape([nz,nx]) 
            logger.info('using vs %f' % vs[0,0])

        data['vrup'] = compute_rupture_velocity( data['trup'], dx ) / 3464.
        data['sum']  = np.sqrt( data['su1']**2 + data['su2']**2 )
        data['mu0']  = data['tsm'] / np.absolute(data['tnm'])
        data['dtau'] = _compute_stress_drop( files['tsm'], tsm_field['shape'], dtype )

        # store information about the rupture on the fault
        simulation['rupture'] = {
            'fault_extent' : _get_fault_extent( data['psv'], nx, nz, dx ),
            'magnitude'    : _read_magnitude( cwd, dtype ),
            'del_tau'      : data['dtau'].mean() / 1e6
        }
    except Exception as e:
        logger.error(e)
        # set state to failed
        return

    """ plot kinematic fields """
    clabel = {
        'su1' : r'$u_x$ (m)',
        'su2' : r'$u_z$ (m)',
        'trup': r'$t_{rup}$ (s)',
        'psv' : r'$V_{peak} (m/s)$',
        'tsm' : r'$|\tau_s| (MPa)$',
        'tnm' : r'$|\tau_n| (MPa)$',
        'vrup': r'$v_{rup}$ (m/s)',
        'sum' : r'$|u| (m)$',
        'mu0' : r'$\mu_0$',
        'dtau' : r'$\Delta \tau$' # needs some work
    }

    # set up list of figures for database
    figs = []
    media_root = os.path.join( os.path.dirname(os.path.realpath(__file__)), 'media/visualize/models/' )
    for key in clabel:
        figs.append( {'name': key, 
                      'file_path': os.path.join(media_root, 
                            simulation['parameters']['name'] + "_" + key + '.png' )    
                      } )

    # manually add variogram figure because it comes from R
    figs.append( {'name': 'vario',
                  'file_path': os.path.join(media_root, 
                        simulation['parameters']['name'] + '_vario.png' )
                  } )

    # manually add histogram
    figs.append( {'name': 'hist',
                  'file_path': os.path.join(media_root, 
                        simulation['parameters']['name'] + '_hist.png' )
                  } )

    # manually add variogram figure because it comes from R
    figs.append( {'name': 'hist_log',
                  'file_path': os.path.join(media_root, 
                        simulation['parameters']['name'] + '_hist_log.png' )
                  } )


    # plot figures i think we want them in both places for posterity
    for field in data:
        if field not in ['x','z']:
            if field in ['sum','su1','su2']:
                inp = { 'data'    : data[field], 
                        'contour' : data['trup'] }
                plot_2d_image( inp, filename=os.path.join(figdir, field + '.png'),
                    nx=nx, nz=nz, dx=dx*1e-3, clabel=clabel[field], xlabel='Distance (km)', ylabel='Depth (km)', 
                    surface_plot=True, contour=True )
            elif field == 'vrup':
                plot_2d_image( data[field], filename=os.path.join(figdir, field + '.png'),
                    nx=nx, nz=nz, dx=dx*1e-3, clabel=clabel[field], xlabel='Distance (km)', ylabel='Depth (km)', 
                    surface_plot=False, contour=False, clim = [0.5, 1.0] )
            else:
                plot_2d_image( data[field], filename=os.path.join(figdir, field + '.png'),
                        nx=nx, nz=nz, dx=dx*1e-3, clabel=clabel[field], xlabel='Distance (km)', ylabel='Depth (km)', 
                        surface_plot=False, contour=False )


    """ calculate one-point statistics 
    mask unwanted values 
        1) inside hypocenter 
        2) inside velocity-strengthening 
        3) where super-shear 
        4) within rupturing area on the fault

    compute slip.mean(), slip.std(), psv.mean(), psv.std(), vrup.mean(), vrup.std(), commit to data structure
    """
    
    include = ['sum', 'vrup', 'psv', 'mu0', 'x', 'z', 'dtau']
    temp = {}
    for key in data:
        if key in include:
            temp[key] = data[key].ravel()

    # write old data
    data = pd.DataFrame( data = temp ) 
    rcrit = np.max([simulation['parameters']['rnucl'], simulation['parameters']['rcrit']])
    """ kind of complex?, but it crops the source region and some other obvious things.  """
    data_trimmed =  pd.concat(
                    [ data[
                     ( ( (data['x'] > ihypo[0]-rcrit) & (data['x'] < ihypo[0]+rcrit) )   & 
                       ( (data['z'] < ihypo[1]-rcrit) | (data['z'] > ihypo[1]+rcrit) ) ) &
                    ( (data['z'] > 0) & (data['z'] < 15000) ) &
                    ( (data['vrup'] < 1.0) & (data['vrup'] > 0.0) ) &
                    ( data['psv'] > 0.4 ) ],

                    data[((data['x'] < ihypo[0]-rcrit) | (data['x'] > ihypo[0]+rcrit)) &
                    ( (data['z'] > 0) & (data['z'] < 15000) ) &
                    ( data['psv'] > 0.4 )  &
                    ( (data['vrup'] < 1.0) & data['vrup'] > 0.0 )] ]).drop_duplicates()


    if len(data_trimmed) < 10000:
        logger.warning("less that 10,000 datapoints, not sampling.")
        data_sample = data_trimmed
    else:
        data_sample = data_trimmed.sample( n=10000 )

    # store one-point statistics
    simulation['one_point'] = {

        # same sampled version
        'avg_slip_tr': data_trimmed['sum'].mean(),
        'avg_psv_tr':  data_trimmed['psv'].mean(),
        'avg_vrup_tr': data_trimmed['vrup'].mean(),
        'std_slip_tr': data_trimmed['sum'].std(),
        'std_psv_tr': data_trimmed['psv'].std(),
        'std_vrup_tr': data_trimmed['vrup'].std(),

        # save sampled version
        'avg_slip_sa': data_sample['sum'].mean(),
        'avg_psv_sa':  data_sample['psv'].mean(),
        'avg_vrup_sa': data_sample['vrup'].mean(),
        'std_slip_sa': data_sample['sum'].std(),
        'std_psv_sa': data_sample['psv'].std(),
        'std_vrup_sa': data_sample['vrup'].std(),

        # save median version
        'med_slip_sa': data_sample['sum'].median(),
        'med_psv_sa':  data_sample['psv'].median(),
        'med_vrup_sa': data_sample['vrup'].median(),
        'mad_slip_sa': data_sample['sum'].mad(),
        'mad_psv_sa': data_sample['psv'].mad(),
        'mad_vrup_sa': data_sample['vrup'].mad(),

        # save median of stress drop
        'med_del_tau': data_trimmed['dtau'].median() / 1e6,
        'avg_del_tau': data_trimmed['dtau'].mean() / 1e6

    }

    # calculate two-point statistics
    """ stored in directory vario """
    subprocess.call(["Rscript", os.path.join(cwd, "analysis.R"), cwd])

    # copy figures to media root
    for fig in figs:
        src = os.path.join( figdir, fig['name'] + '.png' )
        shutil.copy( src, fig['file_path'] )


    # compute histograms 
    ax = data_sample.hist( 
            bins = np.sqrt(len(data_sample.index)), 
            normed = 1, 
            column = ['mu0','sum','psv','vrup'], 
    )
    fig = _get_figure( ax )
    fig.savefig( os.path.join( figdir, 'hist.png' ), dpi=300 )

    ax = np.log10(data_sample).hist( 
            bins = np.sqrt(len(data_sample.index)), 
            normed = 1, 
            column = ['mu0','sum','psv','vrup'], 
    )
    fig = _get_figure( ax )
    fig.savefig( os.path.join( figdir, 'hist_log.png' ), dpi=300 )


    """ write out csv files """
    # # print 'writing csv files'
    logger.info('writing csv files')
    data_trimmed.to_csv( os.path.join(datadir, 'data_trimmed.csv') )
    data_sample.to_csv( os.path.join(datadir, 'data_sampled.csv') )
    one_point = pd.Series( simulation['one_point'] ).to_csv( os.path.join(datadir, 'one_point.csv') )

    logger.info('saving to database')
    sim = _get_or_none( Simulation, simulation['parameters']['name'] )
    
    # check if simulation with same name exists already
    if sim:
        logger.info('simulation with name %s exists, updating entry.' % simulation['simulation']['name'])
        simulation_form = SimulationForm( simulation['simulation'], instance = sim )
    else:
        logger.info('making new database entry for simulation %s' % simulation['simulation']['name'])
        simulation_form = SimulationForm( simulation['simulation'] )

    # validate simulation form
    if simulation_form.is_valid():
        new_simulation = simulation_form.save()
        logger.info('saved simulation to database')
    else:
        logger.error('unable to save simulation, aborting.')
        return
    
    # create new forms for various tables given instance new_simulation 
    # forms = [ SimulationOutputForm, SimulationInputForm, ParametersForm, RuptureParametersForm ]
    # data = [ simulation['fieldio']['outputs'], simulation['fieldio']['inputs'], simulation['parameters'], simulation['rupture'] ]
    # forms = [ ParametersForm ]
    # data = [ simulation['parameters'] ]
    # # form should be dict or list of dicts
    # for f, d in zip(forms, data):
    #     _commit_form_with_fk( f, d, new_simulation )
    
    # forms = [ ParametersForm, RuptureParametersForm ]
    # data = [{key: val.__repr__() for (key, val) in simulation['parameters'].items()}, 
    #         simulation['rupture'], ] 
    forms = [ ParametersForm, RuptureParametersForm, OnePointForm, FigureForm, SimulationInputForm, SimulationOutputForm ]
    data = [ {key: val.__repr__() for (key, val) in simulation['parameters'].items()},
             simulation['rupture'], 
             simulation['one_point'],
             figs,
             simulation['fieldio']['inputs'],
             simulation['fieldio']['outputs'] ] 

    # commit the forms
    for f, d in zip(forms, data):
        _commit_form_with_fk( f, d, new_simulation ) 

"""
Functions
"""
def _get_or_none( model_class, name, **kwargs ):
    from django.core.exceptions import ObjectDoesNotExist
    try:
        query = model_class.objects.get( name = name, **kwargs )
    except ObjectDoesNotExist:
        query = None
    return query


def _commit_form_with_fk( form, data, instance ):
    # we can just commit a dict
    import logging as logger
    if isinstance(data, dict):
        f = form( data )
        if f.is_valid():
            m = f.save( commit = False )
            m.simulation = instance
            m.save()
            logger.info('saved %s to database' % str(m) )
        else:
            print f.errors
    # must loop over dicts
    else:
        for d in data:
            f = form( d )
            if f.is_valid():
                m = f.save( commit = False )
                m.simulation = instance
                m.save()
                logger.info('saved %s to database' % str(m) )
            else:
                print f.errors

def _get_figure( ax ):
    return ax[0,0].get_figure()

def _compute_stress_drop( file , shape, dtype ): 
    from numpy import fromfile
    import os
    nx = shape[0]
    nz = shape[1]
    nt = shape[2]
    ts = fromfile( file, dtype=dtype, count = nx*nz ).reshape( [nz, nx] )
    fh = open( file, 'rb' )
    fh.seek( -nx*nz*4, 2 )
    tsf = fromfile( fh, dtype=dtype ).reshape([nz,nx])
    delt = tsf - ts
    return delt

def _parse_simulation_details( cwd, write = False ):
    import os
    import logging
    # data structure for simulation.
    data = {}
    data['simulation'] = {}
    data['parameters'] = {}
    data['fieldio'] = {}
    # read meta.py file
    try:
        # this is dangerous, should change to xml, or yaml
        exec( open( os.path.join(cwd, 'meta.py')).read() )
        # get list of local variables aka namespace of meta.py
        lvars = locals()
        exclude = ['json', 'lvars', 'shape', 'xi', 'indices', 'os', 'logging', 'data']
        for var, val in lvars.items():
            # exclude builtin types and json import
            if not var.startswith('__') and var not in exclude:
                if var == 'fieldio':
                    #print 'parsing fieldio'
                    inputs, outputs = _parse_fieldio(val, eval('shape'), eval('indices'))
                    data['fieldio']['inputs'] = inputs
                    data['fieldio']['outputs'] = outputs
                else:
                    data['parameters'][var] = eval(var)

        
        # write json file containing simulation data
        if write:
            import json
            with open('test2.js', 'w') as fh:
                json.dump(data, fh, indent=2)
    
    except Exception as e:
        logger.error('cannot read simulation details. error: %s' % str(e)) 
        return data
    
    # to be consistent with models
    data['simulation']['name'] = data['parameters']['name']
    data['simulation']['user'] = data['parameters']['user']

    return data

"""turns meta.py file into json object using eval, this is very risky, but I trust myself"""
def _parse_fieldio(fieldio, shape, indices):
    inputs = []
    outputs = []
    for field in fieldio:
        # outputs
        field_vals = field[-3:]
        if field[0] == '=w':
            outputs.append( {
                'file': field_vals[0],
                'field': field_vals[2][0],
                'shape': shape[str(field_vals[0])],
                'indices': indices[str(field_vals[0])],
                } )

        # inputs
        if field[0] == '=R' or field[0] == "=r":
            inputs.append( {
                'file': field_vals[0],
                'field': field_vals[2][0],
                'val': ''

             } )
    
        # also inputs
        if field[0] == '=':
            inputs.append( {
                'file': '',
                'field': field_vals[2][0],
                'val': field_vals[1],
                } )
        
    return inputs, outputs



def _read_magnitude( cwd, dtype ):
    import os
    from numpy import fromfile, where

    # try finding that file anywhere in the model directory
    for root, dirs, files in os.walk( cwd ):
        for name in files:
            if name == 'mw':
                mw = fromfile(os.path.join(root, name),dtype=dtype)[-1]
                return mw
    raise IOError

# try using this function with trup to get proper fault extent
def _get_fault_extent( field, nx, nz, dx ):
    """Needs work... Functional for now."""
    import os
    from numpy import where, floor

    y, x = where( field > 1.0 ) # returns inds where condition is true
    strtx = x.min()
    endx = x.max()
    nflt = floor( (endx - strtx) / 2 )
    if nflt < 0:
        print 'negative fault length, something is wrong.'
        raise ValueError
    fault_len = nflt * dx 
    return fault_len

	
