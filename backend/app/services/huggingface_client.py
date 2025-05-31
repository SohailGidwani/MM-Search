"""Client for HuggingFace models."""
import logging
from typing import List

from transformers import pipeline
import torch

logger = logging.getLogger(__name__)


class HuggingFaceClient:
    """Wrapper around HuggingFace models."""

    def __init__(self, model_name: str = "facebook/s2t-small-librispeech-asr") -> None:
        self.model_name = model_name
        self._asr = pipeline(
            "automatic-speech-recognition",
            model=self.model_name,
            device=0 if torch.cuda.is_available() else -1,
        )

    def transcribe(self, audio_path: str) -> str:
        """Transcribe audio file."""
        try:
            result = self._asr(audio_path)
            return result.get("text", "")
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("ASR failed: %s", exc)
            return ""
