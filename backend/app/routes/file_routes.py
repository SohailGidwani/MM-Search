# app/routes/file_routes.py
import os, mimetypes
from flask import Blueprint, jsonify, send_file, abort
from app.models.file_model import File
from app.utils.logger import logger_msg
from app import db

file_bp = Blueprint('file_bp', __name__)

@file_bp.route('/<int:file_id>', methods=['GET'])
def get_file_meta(file_id: int):
    rec = db.session.get(File, file_id)
    if not rec:
        return jsonify({"error": "Not found"}), 404
    return jsonify({
        "id":   rec.id,
        "name": rec.original_filename,
        "type": rec.file_type,
        "size": rec.file_size,
        "path": rec.file_path,
        "status": rec.processing_status
    })

@file_bp.route('/<int:file_id>/download', methods=['GET'])
def download_file(file_id: int):
    rec = db.session.get(File, file_id)
    if not rec or not os.path.exists(rec.file_path):
        return abort(404)
    mime, _ = mimetypes.guess_type(rec.file_path)
    logger_msg(f"Downloading file_id={file_id}", "info")
    return send_file(rec.file_path, mimetype=mime,
                     as_attachment=True,
                     download_name=rec.original_filename)