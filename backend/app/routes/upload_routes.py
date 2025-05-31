"""Upload endpoints."""
import logging
from pathlib import Path

from flask import Blueprint, current_app, request, jsonify
from werkzeug.utils import secure_filename

from .. import db
from ..models import File

upload_bp = Blueprint('upload', __name__)
logger = logging.getLogger(__name__)


@upload_bp.route('/file', methods=['POST'])
def upload_file():
    """Upload a single file."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    filename = secure_filename(file.filename)
    upload_folder = current_app.config['UPLOAD_FOLDER']
    Path(upload_folder).mkdir(parents=True, exist_ok=True)
    filepath = Path(upload_folder) / filename
    file.save(filepath)

    file_record = File(
        filename=filename,
        original_filename=file.filename,
        file_path=str(filepath),
        file_type=file.content_type,
        file_size=Path(filepath).stat().st_size,
        mime_type=file.content_type,
    )
    db.session.add(file_record)
    db.session.commit()

    # schedule processing
    from ..scheduler.tasks import schedule_processing
    schedule_processing(file_record.id)

    return jsonify({'file_id': file_record.id}), 201


@upload_bp.route('/batch', methods=['POST'])
def upload_batch():
    """Upload multiple files."""
    files = request.files.getlist('files')
    ids = []
    for file in files:
        filename = secure_filename(file.filename)
        upload_folder = current_app.config['UPLOAD_FOLDER']
        Path(upload_folder).mkdir(parents=True, exist_ok=True)
        filepath = Path(upload_folder) / filename
        file.save(filepath)
        record = File(
            filename=filename,
            original_filename=file.filename,
            file_path=str(filepath),
            file_type=file.content_type,
            file_size=Path(filepath).stat().st_size,
            mime_type=file.content_type,
        )
        db.session.add(record)
        db.session.commit()
        from ..scheduler.tasks import schedule_processing
        schedule_processing(record.id)
        ids.append(record.id)
    return jsonify({'file_ids': ids}), 201


@upload_bp.route('/status/<int:file_id>', methods=['GET'])
def upload_status(file_id: int):
    """Return processing status."""
    file_record = File.query.get_or_404(file_id)
    return jsonify({'status': file_record.processing_status})
