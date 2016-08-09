import os
import subprocess
import logging
import time

from workers import SimpleTask
from managers import SimpleTaskWorkerManager  
from tasks.dynamic_rupture_task import process_dynamic_rupture_simulation

# TODO: commit information about models to the database (clean-up process).
# TODO: design templates to show models using html (initially markdown).
# TODO: state-machine to keep track of tasks and states of workers, etc.

def process_and_upload_simulations( files ):
    """ wrapper used to process dynamic rupture simulations """
    print files
    home_dir = os.path.dirname(os.path.realpath(__file__))
    params = { 
               'home_dir' : home_dir, 
               'script_dir' : os.path.join(home_dir, 'utils')
             }
             
    """ initialize log in directory above root_dir and record year, month, day """
    logging.basicConfig( filename = os.path.join( os.getcwd(), 
                                            'tasks-log' + time.strftime("%Y%m%d") + '.log' ),
                         level = logging.INFO 
                       )

    """ get access to a task manager """
    group = SimpleTaskWorkerManager( max_workers = 2 )

    """ define tasks that are applied to each simulation;
        eventually build parameter file that lets user specify what tasks to run, etc.
     """
    individual_tasks = [
                        process_dynamic_rupture_simulation
                        # plot_gmpe,
                        # calc_gmpe,
                        # one_point_statistics,
                        # plot_kinematic_fields,
                       ]

    """ apply tasks to group """
    _queue_individual_tasks( group, individual_tasks, files, params )

    # """ define and apply tasks that are applied to all simulations """
    # group.add_task_to_queue( SimpleTask( plot_gmpe_group_bias, params=params ) )
    group.start_working()
    group.wait_all()

    print 'All Finished!'

def _queue_individual_tasks( group, tasks, files, params ):
    """
    Queues tasks that will be applied to every model. For instance, "plot_gmpe" or "calc_one_point_statistics."

    Parameters:
        group (WorkGroup) : workgroup for tasks
        tasks (list) : list of tasks 
        params (dict) : 
    """
    if tasks and files:
        for file in files:
            if file:
                for task in tasks:
                    params['cwd'] = file
                    task = SimpleTask( task, params=params )
                    if task.ready():
                        group.add_task_to_queue( task )

