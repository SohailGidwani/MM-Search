"""File management routes."""
from flask import Blueprint, jsonify, abort

from ..models import File

file_bp = Blueprint('files', __name__)


@file_bp.route('', methods=['GET'])
def list_files():
    """List uploaded files."""
    files = File.query.all()
    return jsonify([{'id': f.id, 'filename': f.filename, 'status': f.processing_status} for f in files])


@file_bp.route('/<int:file_id>', methods=['GET'])
def get_file(file_id: int):
    """Get file details."""
    file_record = File.query.get_or_404(file_id)
    return jsonify({'id': file_record.id, 'filename': file_record.filename, 'status': file_record.processing_status})


@file_bp.route('/<int:file_id>', methods=['DELETE'])
def delete_file(file_id: int):
    """Delete file."""
    file_record = File.query.get_or_404(file_id)
    File.query.filter_by(id=file_id).delete()
    from .. import db
    db.session.commit()
    return jsonify({'deleted': file_id})


@file_bp.route('/<int:file_id>/content', methods=['GET'])
def file_content(file_id: int):
    """Get processed content."""
    file_record = File.query.get_or_404(file_id)
    return jsonify({'chunks': [{'id': c.id, 'text': c.content_text} for c in file_record.chunks]})
