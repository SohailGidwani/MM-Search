"""Search service."""
import logging
from typing import List

from qdrant_client import QdrantClient
from flask import current_app

from ..models import SearchLog
from .. import db

logger = logging.getLogger(__name__)


class SearchService:
    """Search across embeddings."""

    def __init__(self) -> None:
        self.qdrant = QdrantClient(url=current_app.config['QDRANT_URL'])

    def search(self, query: str, limit: int = 5) -> List[dict]:
        """Perform semantic search."""
        # naive implementation using text_embeddings only
        vector = []
        results: List[dict] = []
        try:
            # Here we would call Ollama to embed the query
            from .ollama_client import OllamaClient
            vector = OllamaClient().embed_text(query)
            if vector:
                search_result = self.qdrant.search(collection_name='text_embeddings', query_vector=vector, limit=limit)
                results = [hit.payload for hit in search_result]
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Search failed: %s", exc)
        db.session.add(SearchLog(query=query, results_count=len(results)))
        db.session.commit()
        return results
