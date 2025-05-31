"""Background processing tasks."""
import logging
from flask import current_app, Flask

from .. import scheduler
from ..services.processing_service import ProcessingService

logger = logging.getLogger(__name__)


def schedule_processing(file_id: int) -> None:
    """Schedule file processing job."""
    job_id = f"process_file_{file_id}"
    app = current_app._get_current_object()
    scheduler.add_job(id=job_id, func=process_file_job, trigger='date', args=[file_id, app])


def process_file_job(file_id: int, app: Flask) -> None:
    """Process file job."""
    with app.app_context():
        service = ProcessingService()
        service.process(file_id)
