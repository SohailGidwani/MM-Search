# app/utils/file_processor.py
import os, mimetypes
from datetime import datetime
from app.utils.logger import logger_msg
from app.models.file_model import db, File
from app.services.embedding_service import EmbeddingService

def _get_or_create_file_record(file_path: str) -> File:
    rec = File.query.filter_by(file_path=file_path).first()
    if rec: return rec

    stat = os.stat(file_path)
    mime, _ = mimetypes.guess_type(file_path)
    rec = File(
        filename          = os.path.basename(file_path),
        original_filename = os.path.basename(file_path),
        file_path         = file_path,
        file_type         = mime.split('/')[0] if mime else 'unknown',
        file_size         = stat.st_size,
        mime_type         = mime,
        processing_status = 'processing',
        created_at        = datetime.utcnow(),
    )
    db.session.add(rec); db.session.commit()
    return rec

def process_file(file_path: str) -> dict:
    mime_type, _ = mimetypes.guess_type(file_path)
    rec          = _get_or_create_file_record(file_path)
    out          = {"file_id": rec.id, "mime": mime_type}

    try:
        if not mime_type:
            raise ValueError("Unknown MIME")

        kind = mime_type.split('/')[0]

        if kind == 'image':
            desc = EmbeddingService.store_image(rec.id, file_path)
            out["description"] = desc

        elif kind == 'audio':
            transcript = EmbeddingService.store_audio(rec.id, file_path)
            out["transcription"] = transcript

        elif kind == 'video':
            summary = EmbeddingService.store_video(rec.id, file_path)
            out["video_summary"] = summary

        elif mime_type in ('text/plain',
                           'application/pdf',
                           'application/vnd.openxmlformats-officedocument.wordprocessingml.document'):
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as fh:
                text = fh.read()
            EmbeddingService.store_text(rec.id, text)
            out["text_len"] = len(text)

        else:
            out["warning"] = f"Unsupported MIME {mime_type}"
            logger_msg(out["warning"], "warning")

        rec.processing_status = 'done'
        db.session.commit()
    except Exception as e:
        rec.processing_status = 'failed'
        db.session.commit()
        logger_msg(f"Processing error: {e}", "error")
        out["error"] = str(e)

    return out