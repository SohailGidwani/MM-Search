# app/services/embedding_service.py
from app.services.ollama_client  import OllamaClient
from app.services.vector_service import VectorService
from app.utils.logger     import logger_msg
from app.models.file_model import db, ContentChunk

class EmbeddingService:
    """Persists chunks & pushes their vectors to Qdrant."""

    # ---------- TEXT ----------
    @staticmethod
    def store_text(file_id: int, text: str, idx: int = 0):
        chunk = ContentChunk(file_id=file_id,
                             chunk_type='text',
                             content_text=text,
                             chunk_index=idx)
        db.session.add(chunk); db.session.commit()

        vec = OllamaClient.get_text_embeddings(text)
        pid = VectorService.upsert("text_embeddings", vec,
                                   {"file_id": file_id,
                                    "chunk_id": chunk.id,
                                    "type": "text"})
        chunk.vector_id = pid
        db.session.commit()
        logger_msg(f"text chunk stored → point {pid}", "debug")

    # ---------- IMAGE ----------
    @staticmethod
    def store_image(file_id: int, image_path: str, idx: int = 0):
        desc = OllamaClient.describe_image(image_path)
        EmbeddingService.store_text(file_id, desc, idx)  # reuse text pathway
        return desc

    # ---------- AUDIO ----------
    @staticmethod
    def store_audio(file_id: int, audio_path: str):
        transcript = OllamaClient.transcribe_audio(audio_path)
        EmbeddingService.store_text(file_id, transcript, 0)
        return transcript

    # ---------- VIDEO ----------
    @staticmethod
    def store_video(file_id: int, video_path: str):
        summary = OllamaClient.describe_video(video_path)
        EmbeddingService.store_text(file_id, summary, 0)
        return summary