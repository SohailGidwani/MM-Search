from celery import shared_task
from app.utils.logger import logger_msg
from app.utils.file_processor import process_file

@shared_task(bind=True)
def process_file_task(self, file_path):
    try:
        logger_msg(f"Processing file: {file_path}", "info")
        result = process_file(file_path)
        logger_msg(f"Processing completed: {file_path}", "info")
        return result
    except Exception as e:
        logger_msg(f"Processing failed: {e}", "error")
        raise self.retry(exc=e, countdown=60, max_retries=3)