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
        vector = self.ollama.embed_text(text)
        if not vector:
            return ''
        try:
            collection = 'text_embeddings'
            response = self.qdrant.upload_collection(collection_name=collection, vectors=[vector], payload=[metadata])
            return response[0]
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Embedding upload failed: %s", exc)
            return ''
