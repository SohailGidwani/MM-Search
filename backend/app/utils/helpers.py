"""Misc helper functions."""
import hashlib
from typing import Any


def hash_string(value: str) -> str:
    """Return sha256 hash of given string."""
    return hashlib.sha256(value.encode('utf-8')).hexdigest()
