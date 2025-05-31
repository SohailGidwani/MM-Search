"""Service for handling embeddings."""
import logging
from typing import List

from qdrant_client import QdrantClient
from flask import current_app

from .ollama_client import OllamaClient

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Manage embeddings using Qdrant."""

    def __init__(self, client: QdrantClient | None = None) -> None:
        self.qdrant = client or QdrantClient(url=current_app.config['QDRANT_URL'])
        self.ollama = OllamaClient()

    def embed_text(self, text: str, metadata: dict) -> str:
        """Embed text and store in Qdrant."""
        logger.debug("Embedding text: %s", text)
        vector = self.ollama.embed_text(text)
        logger.debug("Generated embedding length: %d", len(vector))
        if not vector:
            logger.warning("No embedding generated for text")
            return ''
        try:
            collection = 'text_embeddings'
            logger.debug("Uploading embedding to Qdrant with metadata: %s", metadata)
            response = self.qdrant.upload_collection(
                collection_name=collection,
                vectors=[vector],
                payload=[metadata],
            )
            vector_id = response[0]
            logger.debug("Uploaded vector id: %s", vector_id)
            return vector_id
        except Exception as exc:  # pylint: disable=broad-except
            logger.exception("Embedding upload failed")
            return ''
