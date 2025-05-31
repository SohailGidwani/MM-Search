import os
from datetime import timedelta

class Config:
    """Base configuration."""

    SECRET_KEY = os.getenv('SECRET_KEY', 'change-me')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/multimodal_search')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    QDRANT_URL = os.getenv('QDRANT_URL', 'http://localhost:6333')
    OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 100 * 1024 * 1024))
    HF_MODEL_CACHE = os.getenv('HF_MODEL_CACHE', 'hf_models_cache')
    SCHEDULER_API_ENABLED = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
