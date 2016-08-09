from celery.decorators import task
from celery.utils.log import get_task_logger

from .processing.main import process_and_upload_simulations

logger = get_task_logger(__name__)
@task(name = "process_simulations_task")
def process_and_upload_simulations_task( files ):
	"""processes simulations uploaded from user"""
	logger.info("processed simulation.")
	return process_and_upload_simulations( files )
	