"""Utilities for processing different file types."""
from pathlib import Path
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


def _read_text_file(path: Path) -> str:
    """Return text from a plain text file."""
    return path.read_text(errors="ignore")


def _read_pdf(path: Path) -> str:
    """Extract text from a PDF file."""
    from PyPDF2 import PdfReader

    reader = PdfReader(str(path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def _read_docx(path: Path) -> str:
    """Extract text from a docx file."""
    from docx import Document

    document = Document(str(path))
    return "\n".join(p.text for p in document.paragraphs)


def _describe_image(path: Path) -> str:
    """Describe an image using Ollama."""
    from ..services.ollama_client import OllamaClient

    client = OllamaClient()
    return client.describe_image(str(path))


def _transcribe_audio(path: Path) -> str:
    """Transcribe audio using HuggingFace ASR."""
    from ..services.huggingface_client import HuggingFaceClient

    client = HuggingFaceClient()
    return client.transcribe(str(path))


def _transcribe_video(path: Path) -> str:
    """Extract audio from video and transcribe."""
    import moviepy.editor as mp

    temp_audio = path.with_suffix(".wav")
    clip = mp.VideoFileClip(str(path))
    clip.audio.write_audiofile(str(temp_audio), logger=None)
    text = _transcribe_audio(temp_audio)
    try:
        temp_audio.unlink()
    except Exception:  # pylint: disable=broad-except
        pass
    return text


def process_file(path: Path) -> List[Dict[str, str]]:
    """Process file and return list of content chunks."""
    logger.debug("Processing file: %s", path)
    ext = path.suffix.lower()
    chunks: List[Dict[str, str]] = []
    try:
        if ext == ".txt":
            chunks.append({"type": "text", "content": _read_text_file(path)})
        elif ext == ".pdf":
            chunks.append({"type": "text", "content": _read_pdf(path)})
        elif ext == ".docx":
            chunks.append({"type": "text", "content": _read_docx(path)})
        elif ext in {".png", ".jpg", ".jpeg"}:
            chunks.append({"type": "image", "content": _describe_image(path)})
        elif ext in {".wav", ".mp3"}:
            chunks.append({"type": "audio", "content": _transcribe_audio(path)})
        elif ext == ".mp4":
            chunks.append({"type": "video", "content": _transcribe_video(path)})
        else:
            chunks.append({"type": "text", "content": _read_text_file(path)})
    except Exception:  # pylint: disable=broad-except
        logger.exception("Failed to process file")
    return chunks
