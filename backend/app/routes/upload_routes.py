from flask import Blueprint, request, jsonify
from app.utils.logger import logger_msg
from app.tasks.processing_tasks import process_file_task
import os

upload_bp = Blueprint('upload_bp', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        logger_msg("No file part in the request.", "error")
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        logger_msg("No selected file.", "error")
        return jsonify({"error": "No selected file"}), 400

    upload_path = os.path.join('uploads', file.filename)
    file.save(upload_path)
    logger_msg(f"File uploaded: {upload_path}", "info")

    # Trigger asynchronous file processing
    task = process_file_task.delay(upload_path)

    return jsonify({"message": "File uploaded and processing started", "task_id": task.id}), 202