"""Redis cache service."""
import logging
import json
from typing import Any

import redis
from flask import current_app

logger = logging.getLogger(__name__)


class CacheService:
    """Simple wrapper around Redis."""

    def __init__(self) -> None:
        self.redis = redis.Redis.from_url(current_app.config['REDIS_URL'])

    def get(self, key: str) -> Any:
        """Get value from cache."""
        logger.debug("Cache GET %s", key)
        value = self.redis.get(key)
        if value is None:
            return None
        return json.loads(value)

    def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        """Set cache value."""
        logger.debug("Cache SET %s ttl=%s", key, ttl)
        self.redis.setex(key, ttl, json.dumps(value))
