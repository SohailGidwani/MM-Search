"""Basic file processing placeholder."""
from pathlib import Path
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


def process_file(path: Path) -> List[Dict[str, str]]:
    """Process file and return chunks."""
    # This is a simplified placeholder that just reads text files
    logger.debug("Processing file: %s", path)
    try:
        text = path.read_text(errors='ignore')
        logger.debug("File text content: %s", text)
        return [{'type': 'text', 'content': text}]
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception("Failed to process file")
        return []
