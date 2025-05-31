"""Search service."""
import logging
from typing import List, Dict

from qdrant_client import QdrantClient
from flask import current_app

from ..models import SearchLog
from .. import db

logger = logging.getLogger(__name__)


class SearchService:
    """Search across embeddings."""

    def __init__(self) -> None:
        self.qdrant = QdrantClient(url=current_app.config['QDRANT_URL'])
        from .ollama_client import OllamaClient
        self.ollama = OllamaClient()

    def search(self, query: str, limit: int = 5) -> Dict[str, object]:
        """Perform semantic search and summarize results."""
        logger.info("Search requested for query: %s", query)
        vector = []
        results: List[dict] = []
        summary = ""
        try:
            vector = self.ollama.embed_text(query)
            logger.debug("Query embedding length: %d", len(vector))
            if vector:
                search_result = self.qdrant.search(
                    collection_name='text_embeddings', query_vector=vector, limit=limit
                )
                results = [hit.payload for hit in search_result]
                logger.debug("Qdrant returned %d results", len(results))

                # gather text from DB for summarization
                from ..models import ContentChunk
                texts = []
                for payload in results:
                    file_id = payload.get('file_id')
                    chunk_idx = payload.get('chunk_id')
                    chunk = ContentChunk.query.filter_by(file_id=file_id, chunk_index=chunk_idx).first()
                    if chunk and chunk.content_text:
                        texts.append(chunk.content_text)
                        logger.debug("Found chunk for summarization: %s", chunk.content_text)
                if texts:
                    context = "\n".join(texts)
                    prompt = (
                        f"Using the following documents, answer the query: '{query}'.\n" + context
                    )
                    logger.debug("Prompt for summarization: %s", prompt)
                    summary = self.ollama.summarize_text(prompt)
                    logger.debug("Summary generated: %s", summary)
        except Exception as exc:  # pylint: disable=broad-except
            logger.exception("Search failed")
        db.session.add(SearchLog(query=query, results_count=len(results)))
        db.session.commit()
        return {"results": results, "summary": summary}
