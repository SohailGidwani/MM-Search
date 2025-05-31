"""File processing service."""
import logging
from pathlib import Path
from typing import Optional

from flask import current_app

from ..models import File
from .. import db
from .embedding_service import EmbeddingService
from ..utils.file_processor import process_file

logger = logging.getLogger(__name__)


class ProcessingService:
    """Handle background file processing."""

    def __init__(self) -> None:
        self.embedding = EmbeddingService()

    def process(self, file_id: int) -> None:
        """Process an uploaded file."""
        file_record: Optional[File] = File.query.get(file_id)
        if not file_record:
            logger.error("File %s not found", file_id)
            return
        logger.info("Processing file %s", file_id)
        file_record.processing_status = 'processing'
        file_record.processing_started_at = db.func.now()
        db.session.commit()

        try:
            chunks = process_file(Path(file_record.file_path))
            logger.debug("Extracted %d chunks from file", len(chunks))
            for idx, chunk in enumerate(chunks):
                logger.debug("Chunk %d content: %s", idx, chunk.get('content'))
                metadata = {
                    'file_id': file_id,
                    'chunk_id': idx,
                    'content_type': chunk['type'],
                    'filename': file_record.filename,
                    'content': chunk['content'],
                }
                vector_id = self.embedding.embed_text(chunk['content'], metadata)
                logger.debug("Vector id returned: %s", vector_id)
                # store chunk in DB
                from ..models import ContentChunk
                db.session.add(ContentChunk(
                    file_id=file_id,
                    chunk_type=chunk['type'],
                    content_text=chunk['content'],
                    chunk_index=idx,
                    related_metadata=metadata,
                    vector_id=vector_id,
                    embedding_model='nomic-embed-text',
                ))
            file_record.processing_status = 'completed'
            file_record.processing_completed_at = db.func.now()
        except Exception as exc:  # pylint: disable=broad-except
            logger.exception("Processing failed")
            file_record.processing_status = 'error'
            file_record.error_message = str(exc)
        db.session.commit()
