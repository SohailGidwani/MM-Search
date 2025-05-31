"""Client for interacting with Ollama API."""
from typing import List
import logging
import requests
from flask import current_app

logger = logging.getLogger(__name__)


class OllamaClient:
    """Simple client for Ollama models."""

    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = base_url or current_app.config['OLLAMA_URL']

    def embed_text(self, text: str) -> List[float]:
        """Generate text embedding."""
        url = f"{self.base_url}/api/embed"
        logger.debug("Requesting embedding for text: %s", text)
        try:
            resp = requests.post(
                url,
                json={"model": "nomic-embed-text", "input": text},
            )
            resp.raise_for_status()
            data = resp.json()
            # Ollama's embed endpoint may return either an "embedding" field
            # or an "embeddings" list when multiple inputs are provided.
            embedding = data.get("embedding")
            if embedding is None:
                embeddings = data.get("embeddings", [])
                if embeddings:
                    embedding = embeddings[0]
                else:
                    embedding = []
            logger.debug("Received embedding of length %d", len(embedding))
            return embedding
        except requests.RequestException:
            logger.exception("Ollama embedding failed")
            return []

    def describe_image(self, image_path: str) -> str:
        """Generate image description."""
        url = f"{self.base_url}/generate"
        files = {"image": open(image_path, 'rb')}
        logger.debug("Requesting image description for %s", image_path)
        try:
            resp = requests.post(url, files=files, json={"model": "llava:7b"})
            resp.raise_for_status()
            description = resp.json().get('description', '')
            logger.debug("Received image description: %s", description)
            return description
        except requests.RequestException as exc:
            logger.exception("Ollama image description failed")
            return ""

    def summarize_text(self, text: str) -> str:
        """Summarize text using llama3.2:3b model."""
        url = f"{self.base_url}/generate"
        payload = {"model": "llama3.2:3b", "prompt": text}
        logger.debug("Requesting summary with prompt: %s", text)
        try:
            resp = requests.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            summary = data.get("response") or data.get("summary", "")
            logger.debug("Received summary: %s", summary)
            return summary
        except requests.RequestException as exc:
            logger.exception("Ollama summarization failed")
            return ""
