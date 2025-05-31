"""Service for handling embeddings."""
import logging

from qdrant_client import QdrantClient
from qdrant_client.http import models
from uuid import uuid4
from flask import current_app

from .ollama_client import OllamaClient

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Manage embeddings using Qdrant."""

    def __init__(self, client: QdrantClient | None = None) -> None:
        self.qdrant = client or QdrantClient(url=current_app.config['QDRANT_URL'])
        self.ollama = OllamaClient()
        self.collection = 'text_embeddings'
        self._ensure_collection()

    def _ensure_collection(self) -> None:
        """Create embeddings collection if missing."""
        try:
            existing = {c.name for c in self.qdrant.get_collections().collections}
            if self.collection not in existing:
                self.qdrant.recreate_collection(
                    collection_name=self.collection,
                    vectors_config=models.VectorParams(
                        size=768,
                        distance=models.Distance.COSINE,
                    ),
                )
                logger.info("Created Qdrant collection %s", self.collection)
        except Exception:  # pylint: disable=broad-except
            logger.exception("Failed to ensure Qdrant collection")

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

            point_id = str(uuid4())
            self.qdrant.upsert(
                collection_name=collection,
                points=[models.PointStruct(id=point_id, vector=vector, payload=metadata)],
            )
            logger.debug("Uploaded vector id: %s", point_id)
            return point_id
        except Exception as exc:  # pylint: disable=broad-except
            logger.exception("Embedding upload failed")
            return ''
