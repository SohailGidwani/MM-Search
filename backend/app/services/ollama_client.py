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
        url = f"{self.base_url}/embed"
        try:
            resp = requests.post(url, json={"model": "nomic-embed-text", "prompt": text})
            resp.raise_for_status()
            return resp.json().get('embedding', [])
        except requests.RequestException as exc:
            logger.error("Ollama embedding failed: %s", exc)
            return []

    def describe_image(self, image_path: str) -> str:
        """Generate image description."""
        url = f"{self.base_url}/generate"
        files = {"image": open(image_path, 'rb')}
        try:
            resp = requests.post(url, files=files, json={"model": "llava:7b"})
            resp.raise_for_status()
            return resp.json().get('description', '')
        except requests.RequestException as exc:
            logger.error("Ollama image description failed: %s", exc)
            return ""

    def summarize_text(self, text: str) -> str:
        """Summarize text using llama3.2:3b model."""
        url = f"{self.base_url}/generate"
        payload = {"model": "llama3.2:3b", "prompt": text}
        try:
            resp = requests.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data.get("response") or data.get("summary", "")
        except requests.RequestException as exc:
            logger.error("Ollama summarization failed: %s", exc)
            return ""
