"""Basic file processing placeholder."""
from pathlib import Path
from typing import List, Dict


def process_file(path: Path) -> List[Dict[str, str]]:
    """Process file and return chunks."""
    # This is a simplified placeholder that just reads text files
    try:
        text = path.read_text(errors='ignore')
        return [{'type': 'text', 'content': text}]
    except Exception:
        return []
