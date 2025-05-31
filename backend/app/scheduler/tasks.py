"""Background processing tasks."""
import logging
from flask import current_app

from .. import scheduler
from ..services.processing_service import ProcessingService

logger = logging.getLogger(__name__)


def schedule_processing(file_id: int) -> None:
    """Schedule file processing job."""
    scheduler.add_job(func=process_file_job, trigger='date', args=[file_id])


def process_file_job(file_id: int) -> None:
    """Process file job."""
    with current_app.app_context():
        service = ProcessingService()
        service.process(file_id)
