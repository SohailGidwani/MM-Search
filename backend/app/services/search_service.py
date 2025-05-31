# app/services/search_service.py
from app.services.ollama_client   import OllamaClient
from app.services.vector_service  import VectorService
from app.models.file_model import ContentChunk, File
from app.utils.logger      import logger_msg
from sqlalchemy import select
from app import db
import time

class SearchService:

    @staticmethod
    def search_text(query: str, top_k: int = 5):
        t0 = time.perf_counter()
        query_vec = OllamaClient.get_text_embeddings(query)
        hits      = VectorService.search("text_embeddings", query_vec, top_k)
        chunk_ids = [hit.payload["chunk_id"] for hit in hits]

        # Fetch metadata from Postgres
        chunks  = db.session.scalars(
                    select(ContentChunk).where(ContentChunk.id.in_(chunk_ids))
                  ).all()

        results = []
        for chunk in chunks:
            file = db.session.get(File, chunk.file_id)
            results.append({
                "file_id":   file.id,
                "filename":  file.original_filename,
                "snippet":   (chunk.content_text[:160] + '…') if chunk.content_text else None,
                "score":     next(h.score for h in hits if h.payload["chunk_id"] == chunk.id)
            })

        latency_ms = int((time.perf_counter() - t0) * 1000)
        logger_msg(f"Search '{query}' returned {len(results)} results in {latency_ms} ms", "info")
        return results, latency_ms