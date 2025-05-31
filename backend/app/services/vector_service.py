# app/services/vector_service.py
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from app.utils.logger import logger_msg
import os, uuid

QDRANT_URL   = os.getenv('QDRANT_URL', 'http://localhost:6333')
COLLECTIONS  = {
    "text_embeddings":   (768,  "Cosine"),
    "image_embeddings":  (4096, "Cosine"),
    "audio_embeddings":  (768,  "Cosine"),
}

class VectorService:
    _client: QdrantClient | None = None

    @classmethod
    def _ensure_client(cls):
        if cls._client is None:
            cls._client = QdrantClient(url=QDRANT_URL)
        return cls._client

    @classmethod
    def _create_collections_if_needed(cls):
        client = cls._ensure_client()
        existing = {c.name for c in client.get_collections().collections}
        for name, (dim, dist) in COLLECTIONS.items():
            if name not in existing:
                logger_msg(f"Creating Qdrant collection '{name}'", "info")
                client.recreate_collection(
                    collection_name=name,
                    vectors_config=qmodels.VectorParams(size=dim,
                                                        distance=dist)
                )

    # ---------- public helpers ----------
    @classmethod
    def upsert(cls, collection: str, vector: list[float], payload: dict) -> str:
        cls._create_collections_if_needed()
        client = cls._ensure_client()
        point_id = str(uuid.uuid4())
        client.upsert(
            collection_name=collection,
            points=[qmodels.PointStruct(id=point_id,
                                        vector=vector,
                                        payload=payload)]
        )
        return point_id

    @classmethod
    def search(cls, collection: str, vector: list[float], top_k: int = 5):
        cls._create_collections_if_needed()
        client = cls._ensure_client()
        return client.search(collection_name=collection,
                             query_vector=vector,
                             limit=top_k)